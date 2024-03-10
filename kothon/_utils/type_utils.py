"""kothon.utils.type_utils"""

from __future__ import annotations

from abc import abstractmethod
from typing import TypeVar, Protocol


class Comparable(Protocol):  # pylint: disable=too-few-public-methods
    """Protocol for annotating comparable types."""

    @abstractmethod
    def __lt__(self: CT, other: CT) -> bool:
        """abstract lesser functions"""


class Addable(Protocol):  # pylint: disable=too-few-public-methods
    """Protocol for annotating addable types."""

    @abstractmethod
    def __add__(self: AT, other: AT) -> AT:
        """abstract add functions"""


CT = TypeVar("CT", bound=Comparable)
AT = TypeVar("AT", bound=Addable)
