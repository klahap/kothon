"""kothon.utils.type_utils"""

from __future__ import annotations

from abc import abstractmethod
from typing import TypeVar, Protocol, Iterator, Any

T_co = TypeVar("T_co", covariant=True)


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


class Iterable(Protocol[T_co]):  # pylint: disable=too-few-public-methods
    """Protocol for annotating iterable types."""

    @abstractmethod
    def __iter__(self: Iterable[T_co]) -> Iterator[T_co]:
        """abstract iter functions"""


CT = TypeVar("CT", bound=Comparable)
AT = TypeVar("AT", bound=Addable)
IT_contra = TypeVar("IT_contra", bound=Iterable[Any], contravariant=True)
