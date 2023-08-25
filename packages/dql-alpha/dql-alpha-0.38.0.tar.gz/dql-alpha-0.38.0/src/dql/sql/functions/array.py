from sqlalchemy.sql.functions import GenericFunction

from dql.sql.types import Float
from dql.sql.utils import compiler_not_implemented


class cosine_distance(GenericFunction):
    type = Float()
    package = "array"
    name = "cosine_distance"
    inherit_cache = True


class euclidean_distance(GenericFunction):
    type = Float()
    package = "array"
    name = "euclidean_distance"
    inherit_cache = True


compiler_not_implemented(cosine_distance)
compiler_not_implemented(euclidean_distance)
