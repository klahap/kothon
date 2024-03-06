"""kothon aggregation functions"""

from typing import Iterable, Optional, TypeVar, Callable

from .._utils.type_utils import CT, AT
from ..iterable.seq import Seq

T = TypeVar("T")
Key = TypeVar("Key")
Value = TypeVar("Value")


def associate(
    sequence: Iterable[T],
    fn: Callable[[T], tuple[Key, Value]],
) -> dict[Key, Value]:
    """
    Transforms each element of the sequence into a key-value pair and aggregates
    the results into a dictionary.

    :param sequence: The sequence
    :param fn: A function that takes an element of type T and returns a tuple of
    two elements, where the first element is the key and the second element is the
    value.
    :return: A dictionary containing the key-value pairs resulting from the
    transformation of each element in the sequence.
    """
    return Seq(sequence).associate(fn)


def associate_by(
    sequence: Iterable[T],
    key_selector: Callable[[T], Key],
) -> dict[Key, T]:
    """
    Creates a dictionary from the sequence by determining the keys using a specified
    key selector function. The values in the dictionary are the elements themselves.

    :param sequence: The sequence
    :param key_selector: A function that takes an element of type T and returns a
    value of type Key that will be used as the key.
    :return: A dictionary where each key is the result of applying the key selector
    function to each element, and each value is the element itself.
    """
    return Seq(sequence).associate_by(key_selector)


def associate_with(
    sequence: Iterable[T],
    value_selector: Callable[[T], Value],
) -> dict[T, Value]:
    """
    Creates a dictionary from the sequence with elements as keys and values
    determined by a specified value selector function.

    :param sequence: The sequence
    :param value_selector: A function that takes an element of type T and returns a
    value of type Value to be associated with the key.
    :return: A dictionary where each key is an element from the sequence, and each
    value is the result of applying the value selector function to that element.
    """
    return Seq(sequence).associate_with(value_selector)


def group_by(
    sequence: Iterable[T],
    key_selector: Callable[[T], Key],
) -> dict[Key, list[T]]:
    """
    Groups the elements of the sequence into a dictionary, with keys determined by
    the specified key selector function. The values are lists containing all
    elements that correspond to each key.

    :param sequence: The sequence
    :param key_selector: A function that takes an element of type T and returns a
    value of type Key to be used as the key.
    :return: A dictionary where each key is the result of applying the key selector
    function to the elements, and each value is a list of elements that share the
    same key.
    """
    return Seq(sequence).group_by(key_selector)


def all_by(sequence: Iterable[T], predicate: Callable[[T], bool]) -> bool:
    """
    Checks if all elements in the sequence satisfy a specified condition.

    :param sequence: The sequence
    :param predicate: A function that evaluates each element in the sequence to a
    boolean value.
    :return: True if all elements satisfy the condition, False otherwise.
    """
    return Seq(sequence).all(predicate)


def none_by(sequence: Iterable[T], predicate: Callable[[T], bool]) -> bool:
    """
    Checks if no elements in the sequence satisfy a specified condition.

    :param sequence: The sequence
    :param predicate: A function that evaluates each element in the sequence to a
    boolean value.
    :return: True if no elements satisfy the condition, False otherwise.
    """
    return Seq(sequence).none(predicate)


def any_by(sequence: Iterable[T], predicate: Callable[[T], bool]) -> bool:
    """
    Checks if any element in the sequence satisfies a specified condition.

    :param sequence: The sequence
    :param predicate: A function that evaluates each element in the sequence to a
    boolean value.
    :return: True if at least one element satisfies the condition, False otherwise.
    """
    return Seq(sequence).any(predicate)


def max_or_none(sequence: Iterable[CT]) -> Optional[CT]:
    """
    Returns the maximum element in the sequence or None if the sequence is empty.

    :param sequence: The sequence
    :return: The maximum element or None if the sequence is empty.
    """
    return Seq(sequence).max_or_none()


def max_by(sequence: Iterable[T], selector: Callable[[T], CT]) -> T:
    """
    Returns an element for which the given function returns the largest value.

    :param sequence: The sequence
    :param selector: A function that returns a comparable value for each element.
    :return: The element that gives the maximum value from the given function.
    :raises ValueError: If the sequence is empty.
    """
    return Seq(sequence).max_by(selector)


def max_by_or_none(
    sequence: Iterable[T],
    selector: Callable[[T], CT],
) -> Optional[T]:
    """
    Returns an element for which the given function returns the largest value or
    None if the sequence is empty.

    :param sequence: The sequence
    :param selector: A function that returns a comparable value for each element.
    :return: The element that gives the maximum value from the given function or
    None if the sequence is empty.
    """
    return Seq(sequence).max_by_or_none(selector)


def min_or_none(sequence: Iterable[CT]) -> Optional[CT]:
    """
    Returns the minimum element in the sequence or None if the sequence is empty.

    :param sequence: The sequence
    :return: The minimum element or None if the sequence is empty.
    """
    return Seq(sequence).min_or_none()


def min_by(sequence: Iterable[T], selector: Callable[[T], CT]) -> T:
    """
    Returns an element for which the given function returns the smallest value.

    :param sequence: The sequence
    :param selector: A function that returns a comparable value for each element.
    :return: The element that gives the smallest value from the given function.
    :raises ValueError: If the sequence is empty.
    """
    return Seq(sequence).min_by(selector)


def min_by_or_none(
    sequence: Iterable[T],
    selector: Callable[[T], CT],
) -> Optional[T]:
    """
    Returns an element for which the given function returns the smallest value or
    None if the sequence is empty.

    :param sequence: The sequence
    :param selector: A function that returns a comparable value for each element.
    :return: The element that gives the smallest value from the given function or
    None if the sequence is empty.
    """
    return Seq(sequence).min_by_or_none(selector)


def single(sequence: Iterable[T]) -> T:
    """
    Returns the single element in the sequence.

    :param sequence: The sequence
    :return: The single element of the sequence.
    :raises ValueError: If the sequence is empty or contains more than one element.
    """
    return Seq(sequence).single()


def single_or_none(sequence: Iterable[T]) -> Optional[T]:
    """
    Returns the single element in the sequence, or None if the sequence is empty or
    contains more than one element.

    :param sequence: The sequence
    :return: The single element of the sequence or None if the sequence is empty or
    contains more than one element.
    """
    return Seq(sequence).single_or_none()


def first(sequence: Iterable[T]) -> T:
    """
    Returns the first element in the sequence.

    :param sequence: The sequence
    :return: The first element of the sequence.
    :raises ValueError: If the sequence is empty.
    """
    return Seq(sequence).first()


def first_or_none(sequence: Iterable[T]) -> Optional[T]:
    """
    Returns the first element in the sequence, or None if the sequence is empty.

    :param sequence: The sequence
    :return: The first element of the sequence or None if the sequence is empty.
    """
    return Seq(sequence).first_or_none()


def last(sequence: Iterable[T]) -> T:
    """
    Returns the last element in the sequence.

    :param sequence: The sequence
    :return: The last element of the sequence.
    :raises ValueError: If the sequence is empty.
    """
    return Seq(sequence).last()


def last_or_none(sequence: Iterable[T]) -> Optional[T]:
    """
    Returns the first element in the sequence, or None if the sequence is empty.

    :param sequence: The sequence
    :return: The first element of the sequence or None if the sequence is empty.
    """
    return Seq(sequence).last_or_none()


def reduce_or_none(
    sequence: Iterable[T], operation: Callable[[T, T], T]
) -> Optional[T]:
    """
    Accumulates value starting with the first element and applying an operation from
    left to right to current accumulator value and each element.

    :param sequence: The sequence
    :param operation: A function that takes two arguments (accumulator, current
    element) and returns a new accumulator value.
    :return: The accumulated value, or None if the sequence is empty.
    """
    return Seq(sequence).reduce_or_none(operation)


def sum_or_none(sequence: Iterable[AT]) -> Optional[AT]:
    """
    Calculates the sum of all elements in the sequence, or returns None if the
    sequence is empty.

    :param sequence: The sequence
    :return: The sum of the sequence elements, or None if the sequence is empty.
    """
    return Seq(sequence).sum_or_none()


def join_to_string(
    sequence: Iterable[T],
    separator: str = ", ",
    prefix: str = "",
    suffix: str = "",
) -> str:
    """
    Concatenates elements of the sequence into a single string with specified
    separators, prefix, and suffix.

    :param sequence: The sequence
    :param separator: The separator string to use between each element.
    :param prefix: The prefix string to add at the beginning.
    :param suffix: The suffix string to add at the end.
    :return: A string representation of the sequence elements.
    """
    return Seq(sequence).join_to_string(
        separator=separator, prefix=prefix, suffix=suffix
    )
