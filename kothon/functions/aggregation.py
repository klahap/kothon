"""kothon aggregation functions"""

from typing import Iterable, Optional, TypeVar, Callable, overload, Union

from .._utils.type_utils import CT, AT
from ..iterable.seq import Seq

T = TypeVar("T")
Key = TypeVar("Key")
Value = TypeVar("Value")


def to_list(sequence: Iterable[T]) -> list[T]:
    """
    Converts a sequence into a list.

    :param sequence: The sequence
    :return: A list containing all elements of the sequence.
    """
    return list(sequence)


def to_set(sequence: Iterable[T]) -> set[T]:
    """
    Converts a sequence into a set.

    :param sequence: The sequence
    :return: A set containing all elements of the sequence.
    """
    return set(sequence)


def to_frozenset(sequence: Iterable[T]) -> frozenset[T]:
    """
    Converts a sequence into a frozenset.

    :param sequence: The sequence
    :return: A set containing all elements of the sequence.
    """
    return frozenset(sequence)


@overload
def associate(
    fn: Callable[[T], tuple[Key, Value]],
    sequence: Iterable[T],
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


@overload
def associate(
    fn: Callable[[T], tuple[Key, Value]],
) -> Callable[[Iterable[T]], dict[Key, Value]]:
    """
    Builds a function that transforms each element of the sequence into a key-value
    pair and aggregates the results into a dictionary.

    :param fn: A function that takes an element of type T and returns a tuple of
    two elements, where the first element is the key and the second element is the
    value.
    :return: Function that transforms each element of the sequence into a key-value
    pair and aggregates the results into a dictionary.
    """


def associate(
    fn: Callable[[T], tuple[Key, Value]],
    sequence: Optional[Iterable[T]] = None,
) -> Union[dict[Key, Value], Callable[[Iterable[T]], dict[Key, Value]]]:
    """
    Transforms each element of the sequence into a key-value pair and aggregates
    the results into a dictionary.

    :param fn: A function that takes an element of type T and returns a tuple of
    two elements, where the first element is the key and the second element is the
    value.
    :param sequence: The sequence. If None, a callable is returned.
    :return: A dictionary containing the key-value pairs resulting from the
    transformation of each element in the sequence.
    """
    if sequence is None:
        return lambda s: Seq(s).associate(fn)
    return Seq(sequence).associate(fn)


@overload
def associate_by(
    key_selector: Callable[[T], Key],
    sequence: Iterable[T],
) -> dict[Key, T]:
    """
    Creates a dictionary from the sequence by determining the keys using a specified
    key selector function. The values in the dictionary are the elements themselves.

    :param key_selector: A function that takes an element of type T and returns a
    value of type Key that will be used as the key.
    :param sequence: The sequence
    :return: A dictionary where each key is the result of applying the key selector
    function to each element, and each value is the element itself.
    """


@overload
def associate_by(
    key_selector: Callable[[T], Key],
) -> Callable[[Iterable[T]], dict[Key, T]]:
    """
    Builds a function that creates a dictionary from the sequence by determining the
    keys using a specified key selector function. The values in the dictionary are the
    elements themselves.

    :param key_selector: A function that takes an element of type T and returns a
    value of type Key that will be used as the key.
    :return: Function that creates a dictionary from the sequence by determining the
    keys using a specified key selector function. The values in the dictionary are the
    elements themselves.
    """


def associate_by(
    key_selector: Callable[[T], Key],
    sequence: Optional[Iterable[T]] = None,
) -> Union[dict[Key, T], Callable[[Iterable[T]], dict[Key, T]]]:
    """
    Creates a dictionary from the sequence by determining the keys using a specified
    key selector function. The values in the dictionary are the elements themselves.

    :param key_selector: A function that takes an element of type T and returns a
    value of type Key that will be used as the key.
    :param sequence: The sequence. If None, a callable is returned.
    :return: A dictionary where each key is the result of applying the key selector
    function to each element, and each value is the element itself.
    """
    if sequence is None:
        return lambda s: Seq(s).associate_by(key_selector)
    return Seq(sequence).associate_by(key_selector)


@overload
def associate_with(
    value_selector: Callable[[T], Value],
    sequence: Iterable[T],
) -> dict[T, Value]:
    """
    Creates a dictionary from the sequence with elements as keys and values
    determined by a specified value selector function.

    :param value_selector: A function that takes an element of type T and returns a
    value of type Value to be associated with the key.
    :param sequence: The sequence. If None, a callable is returned.
    :return: A dictionary where each key is an element from the sequence, and each
    value is the result of applying the value selector function to that element.
    """


@overload
def associate_with(
    value_selector: Callable[[T], Value],
) -> Callable[[Iterable[T]], dict[T, Value]]:
    """
    Builds a function that creates a dictionary from the sequence with elements as
    keys and values determined by a specified value selector function.

    :param value_selector: A function that takes an element of type T and returns a
    value of type Value to be associated with the key.
    :return: Function that creates a dictionary from the sequence with elements as
    keys and values determined by a specified value selector function.
    """


def associate_with(
    value_selector: Callable[[T], Value],
    sequence: Optional[Iterable[T]] = None,
) -> Union[dict[T, Value], Callable[[Iterable[T]], dict[T, Value]]]:
    """
    Creates a dictionary from the sequence with elements as keys and values
    determined by a specified value selector function.

    :param value_selector: A function that takes an element of type T and returns a
    value of type Value to be associated with the key.
    :param sequence: The sequence
    :return: A dictionary where each key is an element from the sequence, and each
    value is the result of applying the value selector function to that element.
    """
    if sequence is None:
        return lambda s: Seq(s).associate_with(value_selector)
    return Seq(sequence).associate_with(value_selector)


@overload
def group_by(
    key_selector: Callable[[T], Key],
    sequence: Iterable[T],
) -> dict[Key, list[T]]:
    """
    Groups the elements of the sequence into a dictionary, with keys determined by
    the specified key selector function. The values are lists containing all
    elements that correspond to each key.

    :param key_selector: A function that takes an element of type T and returns a
    value of type Key to be used as the key.
    :param sequence: The sequence
    :return: A dictionary where each key is the result of applying the key selector
    function to the elements, and each value is a list of elements that share the
    same key.
    """


@overload
def group_by(
    key_selector: Callable[[T], Key],
) -> Callable[[Iterable[T]], dict[Key, list[T]]]:
    """
    Builds a function that groups the elements of the sequence into a dictionary, with
    keys determined by the specified key selector function. The values are lists
    containing all elements that correspond to each key.

    :param key_selector: A function that takes an element of type T and returns a
    value of type Key to be used as the key.
    :return: Function that groups the elements of the sequence into a dictionary, with
    keys determined by the specified key selector function. The values are lists
    containing all elements that correspond to each key.
    """


def group_by(
    key_selector: Callable[[T], Key],
    sequence: Optional[Iterable[T]] = None,
) -> Union[dict[Key, list[T]], Callable[[Iterable[T]], dict[Key, list[T]]]]:
    """
    Groups the elements of the sequence into a dictionary, with keys determined by
    the specified key selector function. The values are lists containing all
    elements that correspond to each key.

    :param key_selector: A function that takes an element of type T and returns a
    value of type Key to be used as the key.
    :param sequence: The sequence. If None, a callable is returned.
    :return: A dictionary where each key is the result of applying the key selector
    function to the elements, and each value is a list of elements that share the
    same key.
    """
    if sequence is None:
        return lambda s: Seq(s).group_by(key_selector)
    return Seq(sequence).group_by(key_selector)


@overload
def all_by(
    predicate: Callable[[T], bool],
    sequence: Iterable[T],
) -> bool:
    """
    Checks if all elements in the sequence satisfy a specified condition.

    :param predicate: A function that evaluates each element in the sequence to a
    boolean value.
    :param sequence: The sequence
    :return: True if all elements satisfy the condition, False otherwise.
    """


@overload
def all_by(predicate: Callable[[T], bool]) -> Callable[[Iterable[T]], bool]:
    """
    Builds a function that checks if all elements in the sequence satisfy a specified
    condition.

    :param predicate: A function that evaluates each element in the sequence to a
    boolean value.
    :return: Function that checks if all elements in the sequence satisfy a specified
    condition.
    """


def all_by(
    predicate: Callable[[T], bool],
    sequence: Optional[Iterable[T]] = None,
) -> Union[bool, Callable[[Iterable[T]], bool]]:
    """
    Checks if all elements in the sequence satisfy a specified condition.

    :param predicate: A function that evaluates each element in the sequence to a
    boolean value.
    :param sequence: The sequence. If None, a callable is returned.
    :return: True if all elements satisfy the condition, False otherwise.
    """
    if sequence is None:
        return lambda s: Seq(s).all(predicate)
    return Seq(sequence).all(predicate)


@overload
def none_by(
    predicate: Callable[[T], bool],
    sequence: Iterable[T],
) -> bool:
    """
    Checks if no elements in the sequence satisfy a specified condition.

    :param predicate: A function that evaluates each element in the sequence to a
    boolean value.
    :param sequence: The sequence
    :return: True if no elements satisfy the condition, False otherwise.
    """


@overload
def none_by(predicate: Callable[[T], bool]) -> Callable[[Iterable[T]], bool]:
    """
    Builds a function that checks if no elements in the sequence satisfy a specified
    condition.

    :param predicate: A function that evaluates each element in the sequence to a
    boolean value.
    :return: Function that checks if no elements in the sequence satisfy a specified
    condition.
    """


def none_by(
    predicate: Callable[[T], bool],
    sequence: Optional[Iterable[T]] = None,
) -> Union[bool, Callable[[Iterable[T]], bool]]:
    """
    Checks if no elements in the sequence satisfy a specified condition.

    :param predicate: A function that evaluates each element in the sequence to a
    boolean value.
    :param sequence: The sequence
    :return: True if no elements satisfy the condition, False otherwise.
    """
    if sequence is None:
        return lambda s: Seq(s).none(predicate)
    return Seq(sequence).none(predicate)


@overload
def any_by(
    predicate: Callable[[T], bool],
    sequence: Iterable[T],
) -> bool:
    """
    Checks if any element in the sequence satisfies a specified condition.

    :param predicate: A function that evaluates each element in the sequence to a
    boolean value.
    :param sequence: The sequence
    :return: True if at least one element satisfies the condition, False otherwise.
    """


@overload
def any_by(predicate: Callable[[T], bool]) -> Callable[[Iterable[T]], bool]:
    """
    Builds a function that checks if any element in the sequence satisfies a specified
    condition.

    :param predicate: A function that evaluates each element in the sequence to a
    boolean value.
    :return: Function that checks if any element in the sequence satisfies a specified
    condition.
    """


def any_by(
    predicate: Callable[[T], bool],
    sequence: Optional[Iterable[T]] = None,
) -> Union[bool, Callable[[Iterable[T]], bool]]:
    """
    Checks if any element in the sequence satisfies a specified condition.

    :param predicate: A function that evaluates each element in the sequence to a
    boolean value.
    :param sequence: The sequence. If None, a callable is returned.
    :return: True if at least one element satisfies the condition, False otherwise.
    """
    if sequence is None:
        return lambda s: Seq(s).any(predicate)
    return Seq(sequence).any(predicate)


def max_or_none(sequence: Iterable[CT]) -> Optional[CT]:
    """
    Returns the maximum element in the sequence or None if the sequence is empty.

    :param sequence: The sequence
    :return: The maximum element or None if the sequence is empty.
    """
    return Seq(sequence).max_or_none()


@overload
def max_by(
    selector: Callable[[T], CT],
    sequence: Iterable[T],
) -> T:
    """
    Returns an element for which the given function returns the largest value.

    :param selector: A function that returns a comparable value for each element.
    :param sequence: The sequence
    :return: The element that gives the maximum value from the given function.
    :raises ValueError: If the sequence is empty.
    """


@overload
def max_by(selector: Callable[[T], CT]) -> Callable[[Iterable[T]], T]:
    """
    Builds a function that returns an element for which the given function returns the
    largest value.

    :param selector: A function that returns a comparable value for each element.
    :return: Function that returns an element for which the given function returns the
    largest value.
    """


def max_by(
    selector: Callable[[T], CT],
    sequence: Optional[Iterable[T]] = None,
) -> Union[T, Callable[[Iterable[T]], T]]:
    """
    Returns an element for which the given function returns the largest value.

    :param selector: A function that returns a comparable value for each element.
    :param sequence: The sequence. If None, a callable is returned.
    :return: The element that gives the maximum value from the given function.
    :raises ValueError: If the sequence is empty.
    """
    if sequence is None:
        return lambda s: Seq(s).max_by(selector)
    return Seq(sequence).max_by(selector)


@overload
def max_by_or_none(
    selector: Callable[[T], CT],
    sequence: Iterable[T],
) -> Optional[T]:
    """
    Returns an element for which the given function returns the largest value or
    None if the sequence is empty.

    :param selector: A function that returns a comparable value for each element.
    :param sequence: The sequence
    :return: The element that gives the maximum value from the given function or
    None if the sequence is empty.
    """


@overload
def max_by_or_none(
    selector: Callable[[T], CT],
) -> Callable[[Iterable[T]], Optional[T]]:
    """
    Builds a function that returns an element for which the given function returns
    the largest value or None if the sequence is empty.

    :param selector: A function that returns a comparable value for each element.
    :return: Function that returns an element for which the given function returns
    the largest value or None if the sequence is empty.
    """


def max_by_or_none(
    selector: Callable[[T], CT],
    sequence: Optional[Iterable[T]] = None,
) -> Union[Optional[T], Callable[[Iterable[T]], Optional[T]]]:
    """
    Returns an element for which the given function returns the largest value or
    None if the sequence is empty.

    :param selector: A function that returns a comparable value for each element.
    :param sequence: The sequence. If None, a callable is returned.
    :return: The element that gives the maximum value from the given function or
    None if the sequence is empty.
    """
    if sequence is None:
        return lambda s: Seq(s).max_by_or_none(selector)
    return Seq(sequence).max_by_or_none(selector)


def min_or_none(sequence: Iterable[CT]) -> Optional[CT]:
    """
    Returns the minimum element in the sequence or None if the sequence is empty.

    :param sequence: The sequence
    :return: The minimum element or None if the sequence is empty.
    """
    return Seq(sequence).min_or_none()


@overload
def min_by(
    selector: Callable[[T], CT],
    sequence: Iterable[T],
) -> T:
    """
    Returns an element for which the given function returns the smallest value.

    :param selector: A function that returns a comparable value for each element.
    :param sequence: The sequence
    :return: The element that gives the smallest value from the given function.
    :raises ValueError: If the sequence is empty.
    """


@overload
def min_by(selector: Callable[[T], CT]) -> Callable[[Iterable[T]], T]:
    """
    Builds a function that returns an element for which the given function returns the
    smallest value.

    :param selector: A function that returns a comparable value for each element.
    :return: Function that returns an element for which the given function returns the
    smallest value.
    """


def min_by(
    selector: Callable[[T], CT],
    sequence: Optional[Iterable[T]] = None,
) -> Union[T, Callable[[Iterable[T]], T]]:
    """
    Returns an element for which the given function returns the smallest value.

    :param selector: A function that returns a comparable value for each element.
    :param sequence: The sequence. If None, a callable is returned.
    :return: The element that gives the smallest value from the given function.
    :raises ValueError: If the sequence is empty.
    """
    if sequence is None:
        return lambda s: Seq(s).min_by(selector)
    return Seq(sequence).min_by(selector)


@overload
def min_by_or_none(
    selector: Callable[[T], CT],
    sequence: Iterable[T],
) -> Optional[T]:
    """
    Returns an element for which the given function returns the smallest value or
    None if the sequence is empty.

    :param selector: A function that returns a comparable value for each element.
    :param sequence: The sequence
    :return: The element that gives the smallest value from the given function or
    None if the sequence is empty.
    """


@overload
def min_by_or_none(
    selector: Callable[[T], CT],
) -> Callable[[Iterable[T]], Optional[T]]:
    """
    Builds a function that returns an element for which the given function returns the
    smallest value or None if the sequence is empty.

    :param selector: A function that returns a comparable value for each element.
    :return: Function that returns an element for which the given function returns the
    smallest value or None if the sequence is empty.
    """


def min_by_or_none(
    selector: Callable[[T], CT],
    sequence: Optional[Iterable[T]] = None,
) -> Union[Optional[T], Callable[[Iterable[T]], Optional[T]]]:
    """
    Returns an element for which the given function returns the smallest value or
    None if the sequence is empty.

    :param selector: A function that returns a comparable value for each element.
    :param sequence: The sequence. If None, a callable is returned.
    :return: The element that gives the smallest value from the given function or
    None if the sequence is empty.
    """
    if sequence is None:
        return lambda s: Seq(s).min_by_or_none(selector)
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


@overload
def reduce_or_none(
    operation: Callable[[T, T], T],
    sequence: Iterable[T],
) -> Optional[T]:
    """
    Accumulates value starting with the first element and applying an operation from
    left to right to current accumulator value and each element.

    :param operation: A function that takes two arguments (accumulator, current
    element) and returns a new accumulator value.
    :param sequence: The sequence
    :return: The accumulated value, or None if the sequence is empty.
    """


@overload
def reduce_or_none(
    operation: Callable[[T, T], T],
) -> Callable[[Iterable[T]], Optional[T]]:
    """
    Builds a function that accumulates value starting with the first element and
    applying an operation from left to right to current accumulator value and each
    element.

    :param operation: A function that takes two arguments (accumulator, current
    element) and returns a new accumulator value.
    :return: Function that accumulates value starting with the first element and
    applying an operation from left to right to current accumulator value and each
    element.
    """


def reduce_or_none(
    operation: Callable[[T, T], T],
    sequence: Optional[Iterable[T]] = None,
) -> Union[Optional[T], Callable[[Iterable[T]], Optional[T]]]:
    """
    Accumulates value starting with the first element and applying an operation from
    left to right to current accumulator value and each element.

    :param operation: A function that takes two arguments (accumulator, current
    element) and returns a new accumulator value.
    :param sequence: The sequence
    :return: The accumulated value, or None if the sequence is empty.
    """
    if sequence is None:
        return lambda s: Seq(s).reduce_or_none(operation)
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
    separator: str = ", ",
    prefix: str = "",
    suffix: str = "",
) -> Callable[[Iterable[T]], str]:
    """
    Builds a function that concatenates elements of the sequence into a single string
    with specified separators, prefix, and suffix.

    :param separator: The separator string to use between each element.
    :param prefix: The prefix string to add at the beginning.
    :param suffix: The suffix string to add at the end.
    :return: Function that concatenates elements of the sequence into a single string
    with specified separators, prefix, and suffix.
    """
    return lambda s: Seq(s).join_to_string(
        separator=separator,
        prefix=prefix,
        suffix=suffix,
    )
