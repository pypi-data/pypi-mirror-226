from datetime import datetime
from typing import *  # type: ignore

from typing_extensions import TypeAlias

from .objectid_proxy import ObjectId

__all__ = [
    "Jsonable",
    "Bsonable",
]


Jsonable: TypeAlias = Union[
    None,
    bool,
    int,
    float,
    str,
    Dict[str, "Jsonable"],
    List["Jsonable"],
    Tuple["Jsonable", ...],
]

JsonDoc = Dict[str, Jsonable]

Bsonable: TypeAlias = Union[
    None,
    bool,
    int,
    float,
    str,
    Dict[str, "Bsonable"],
    List["Bsonable"],
    Tuple["Bsonable", ...],
    bytes,
    ObjectId,
    datetime,
]

BsonDoc = Dict[str, Bsonable]
