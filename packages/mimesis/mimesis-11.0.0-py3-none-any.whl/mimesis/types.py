"""
This module contains knowledge about the types we use.

Policy
~~~~~~

If any of the following statements is true, move the type to this file:

- if type is used in multiple files
- if type is complex enough it has to be documented
- if type is very important for the public API

"""

import datetime
from decimal import Decimal
from typing import Any, Callable, Dict, Final, List, Optional, Set, Tuple, Union

__all__ = [
    "CallableSchema",
    "Date",
    "DateTime",
    "FieldCache",
    "JSON",
    "Key",
    "Keywords",
    "Matrix",
    "MissingSeed",
    "Seed",
    "Time",
    "Timestamp",
]

JSON = Dict[str, Any]

DateTime = datetime.datetime

Time = datetime.time

Date = datetime.date

Timestamp = Union[str, int]


class _MissingSeed:
    """We use this type as a placeholder for cases when seed is not set."""


MissingSeed: Final = _MissingSeed()
Seed = Union[None, int, float, str, bytes, bytearray, _MissingSeed]

Keywords = Union[List[str], Set[str], Tuple[str, ...]]

Number = Union[int, float, complex, Decimal]
Matrix = List[List[Number]]

CallableSchema = Callable[[], JSON]

Key = Optional[Callable[[Any], Any]]

FieldCache = Dict[str, Callable[[Any], Any]]
