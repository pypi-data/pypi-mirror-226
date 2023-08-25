from itertools import chain
from multiprocessing import cpu_count
from sys import stdin
from typing import Any, Dict, Iterator, List, Optional

from dill import load  # nosec B403
from multiprocess import get_context  # pylint: disable=no-name-in-module

from dql.catalog import Catalog
from dql.dataset import DatasetRow
from dql.query.dataset import BATCH_SIZE
from dql.query.udf import UDFFactory

WORKER_BUFFER_SIZE = 1000
STOP_SIGNAL = "STOP"
OK_STATUS = "OK"
FINISHED_STATUS = "FINISHED"
FAILED_STATUS = "FAILED"


def full_module_type_path(typ: type) -> str:
    return f"{typ.__module__}.{typ.__qualname__}"


def udf_entrypoint() -> int:
    # Load UDF info from stdin
    udf_info = load(stdin.buffer)  # nosec B301

    (
        db_adapter_class,
        db_adapter_args,
        db_adapter_kwargs,
    ) = udf_info["data_storage_params"]
    db_adapter = db_adapter_class(*db_adapter_args, **db_adapter_kwargs)
    execute = db_adapter.execute

    # Parallel processing (faster for more CPU-heavy UDFs)
    dispatch = UDFDispatcher(
        udf_info["udf"],
        udf_info["catalog_init"],
        udf_info["data_storage_params"],
    )

    query = udf_info["query"]
    table = udf_info["table"]
    n_workers = udf_info["processes"]
    if n_workers is True:
        # Use default number of CPUs (cores)
        n_workers = None

    selected_columns = [col.name for col in query.selected_columns]
    udf_inputs = (
        DatasetRow.from_result_row(selected_columns, r) for r in execute(query)
    )

    udf_results = dispatch.run_udf_parallel(udf_inputs, n_workers=n_workers)

    rows: List[Dict[str, Any]] = []
    for udf_output in udf_results:
        if not udf_output:
            continue
        rows.extend(udf_output)
        if len(rows) > BATCH_SIZE:
            update = table.insert().values(rows)
            execute(update)
            rows.clear()
    if rows:
        update = table.insert().values(rows)
        execute(update)

    return 0


class UDFDispatcher:
    def __init__(self, udf, catalog_init_params, db_adapter_clone_params):
        # isinstance cannot be used here, as dill packages the entire class definition,
        # and so these two types are not considered exactly equal,
        # even if they have the same import path.
        if full_module_type_path(type(udf)) != full_module_type_path(UDFFactory):
            self.udf = udf
        else:
            self.udf = None
            self.udf_factory = udf
        self.catalog_init_params = catalog_init_params
        (
            self.db_adapter_class,
            self.db_adapter_args,
            self.db_adapter_kwargs,
        ) = db_adapter_clone_params
        self.catalog = None
        self.initialized = False
        self.task_queue = None
        self.done_queue = None
        self.ctx = get_context("spawn")

    def _init_worker(self):
        if not self.catalog:
            db_adapter = self.db_adapter_class(
                *self.db_adapter_args, **self.db_adapter_kwargs
            )
            self.catalog = Catalog(db_adapter, **self.catalog_init_params)
        if not self.udf:
            self.udf = self.udf_factory()
        self.initialized = True

    def _run_worker(self):
        try:
            self._init_worker()
            for row in iter(self.task_queue.get, STOP_SIGNAL):
                udf_output = self._call_udf(row)
                self.done_queue.put({"status": OK_STATUS, "result": udf_output})
            # Finalize UDF, clearing the batch collection and returning
            # any held results
            if udf_output := self._finalize_udf():
                self.done_queue.put({"status": OK_STATUS, "result": udf_output})
            self.done_queue.put({"status": FINISHED_STATUS})
        except Exception as e:
            self.done_queue.put({"status": FAILED_STATUS, "exception": e})
            raise e

    def _call_udf(self, row):
        if not self.initialized:
            raise RuntimeError("Internal Error: Attempted to call uninitialized UDF!")
        return self.udf(self.catalog, row)

    def _finalize_udf(self):
        if not self.initialized:
            raise RuntimeError("Internal Error: Attempted to call uninitialized UDF!")
        if hasattr(self.udf, "finalize"):
            return self.udf.finalize()
        return None

    def run_udf_parallel(
        self, input_rows, n_workers: Optional[int] = None
    ) -> Iterator[List[Dict[str, Any]]]:
        if not n_workers:
            n_workers = cpu_count()
        if n_workers < 1:
            raise RuntimeError(
                "Must use at least one worker for parallel UDF execution!"
            )

        self.task_queue = self.ctx.Queue()
        self.done_queue = self.ctx.Queue()
        # pylint: disable=not-callable
        pool = [
            self.ctx.Process(name=f"Worker-UDF-{i}", target=self._run_worker)
            for i in range(n_workers)
        ]
        for p in pool:
            p.start()

        # Will be set to True if all tasks complete normally
        normal_completion = False
        try:
            # Will be set to True when the input is exhausted
            input_finished = False
            # Stop all workers after the input rows have finished processing
            input_data = chain(input_rows, [STOP_SIGNAL] * n_workers)

            # Add initial buffer of tasks
            for _ in range(WORKER_BUFFER_SIZE):
                try:
                    self.task_queue.put(next(input_data))
                except StopIteration:
                    input_finished = True
                    break

            # Process all tasks
            while n_workers > 0:
                result = self.done_queue.get()
                status = result["status"]
                if status == FINISHED_STATUS:
                    # Worker finished
                    n_workers -= 1
                elif status == OK_STATUS:
                    if not input_finished:
                        try:
                            self.task_queue.put(next(input_data))
                        except StopIteration:
                            input_finished = True
                    yield result["result"]
                else:  # Failed / error
                    n_workers -= 1
                    exc = result.get("exception")
                    if exc:
                        raise exc
                    raise RuntimeError("Internal error: Parallel UDF execution failed")

            # Finished with all tasks normally
            normal_completion = True
        finally:
            if not normal_completion:
                # Stop all workers if there is an unexpected exception
                for _ in pool:
                    self.task_queue.put(STOP_SIGNAL)
                self.task_queue.close()

                # This allows workers (and this process) to exit without
                # consuming any remaining data in the queues.
                # (If they exit due to an exception.)
                self.task_queue.cancel_join_thread()
                self.done_queue.cancel_join_thread()

                # Flush all items from the done queue.
                # This is needed if any workers are still running.
                while n_workers > 0:
                    result = self.done_queue.get()
                    status = result["status"]
                    if status != OK_STATUS:
                        n_workers -= 1

            # Wait for workers to stop
            for p in pool:
                p.join()
