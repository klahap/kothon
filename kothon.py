"""
This script demonstrates the usage of the Seq class for performing a series of
transformations and operations on sequences of data. The Seq class provides a
lazy-evaluation mechanism for efficiently chaining operations such as mapping,
filtering, and reducing sequences.
"""

import random
from typing import TypeVar, Generic, Iterable, Callable, Iterator, Optional, Type
from itertools import islice

T = TypeVar("T")
R = TypeVar("R")
Key = TypeVar("Key")
Value = TypeVar("Value")


class Seq(Generic[T]):
    """
    A sequence class that provides a variety of methods for sequence transformation and
    evaluation, inspired by Kotlin's Sequence type. The Seq class is designed to
    facilitate lazy evaluation of sequences, allowing for efficient chaining of
    operations without creating intermediate collections.
    """

    _iterable: Iterable[T]

    def __init__(self, iterable: Iterable[T]):
        self._iterable = iterable

    def __iter__(self) -> Iterator[T]:
        return iter(self._iterable)

    def filter(self, predicate: Callable[[T], bool]) -> "Seq[T]":
        """
        Filters elements in the sequence based on a predicate.

        :param predicate: A function that evaluates each element to a boolean.
        :return: A new Seq instance with elements that satisfy the predicate.
        """
        return Seq(d for d in self._iterable if predicate(d))

    def filter_not_none(self: "Seq[Optional[R]]") -> "Seq[R]":
        """
        Filters out None values from the sequence.

        :return: A new Seq instance with all elements that are not None.
        """
        return filter_not_none(self._iterable)

    def filter_is_instance(self, cls: Type[R]) -> "Seq[R]":
        """
        Filters elements of the sequence based on their type.

        :param cls: The class type to filter the elements by.
        :return: A new Seq instance containing only elements of the specified type.
        """
        return filter_is_instance(self._iterable, cls)

    def map(self, fn: Callable[[T], R]) -> "Seq[R]":
        """
        Transforms each element in the sequence using a given function.

        :param fn: A function that takes an element of type T and returns an element of
                   type R.
        :return: A new Seq instance with transformed elements.
        """
        return Seq(fn(d) for d in self._iterable)

    def map_not_none(self, fn: Callable[[T], Optional[R]]) -> "Seq[R]":
        """
        Applies a transformation function to each element in the sequence and filters
        out any "None" results.

        :param fn: A function that takes an element of type T and returns an Optional
        element of type R. The function is expected to return "None" for elements that
        should be filtered out.
        :return: A new Seq instance with transformed elements, excluding any "None"
        results.
        """
        return map_not_none(self._iterable, fn)

    def flat_map(self, fn: Callable[[T], Iterable[R]]) -> "Seq[R]":
        """
        Applies a specified function to each element of the sequence that returns an
        iterable, and then flattens the result into a single sequence.

        :param fn: A function that takes an element of type T and returns an Iterable
        of type Iterable[R].
        :return: A new Seq instance containing all the elements from the iterables
        produced by applying the function to each element in the original sequence.
        """
        return flat_map(self._iterable, fn)

    def flatten(self: "Seq[T: Iterable[R]]") -> "Seq[R]":
        """
        Flattens a sequence of iterables into a single sequence.

        The elements of the sequence are expected to be iterables themselves. This
        method concatenates those iterables into a single sequence.

        :return: A new Seq instance containing all the elements of the inner iterables.
        """
        return flatten(self._iterable)

    def associate(self, fn: Callable[[T], tuple[Key, Value]]) -> dict[Key, Value]:
        """
        Transforms each element of the sequence into a key-value pair and aggregates
        the results into a dictionary.

        :param fn: A function that takes an element of type T and returns a tuple of
        two elements, where the first element is the key and the second element is the
        value.
        :return: A dictionary containing the key-value pairs resulting from the
        transformation of each element in the sequence.
        """
        return associate(self._iterable, fn)

    def associate_by(self, key_selector: Callable[[T], Key]) -> dict[Key, T]:
        """
        Creates a dictionary from the sequence by determining the keys using a specified
        key selector function. The values in the dictionary are the elements themselves.

        :param key_selector: A function that takes an element of type T and returns a
        value of type Key that will be used as the key.
        :return: A dictionary where each key is the result of applying the key selector
        function to each element, and each value is the element itself.
        """
        return associate_by(self, key_selector)

    def associate_with(self, value_selector: Callable[[T], Value]) -> dict[T, Value]:
        """
        Creates a dictionary from the sequence with elements as keys and values
        determined by a specified value selector function.

        :param value_selector: A function that takes an element of type T and returns a
        value of type Value to be associated with the key.
        :return: A dictionary where each key is an element from the sequence, and each
        value is the result of applying the value selector function to that element.
        """
        return associate_with(self._iterable, value_selector)

    def group_by(self, key_selector: Callable[[T], Key]) -> dict[Key, list[T]]:
        """
        Groups the elements of the sequence into a dictionary, with keys determined by
        the specified key selector function. The values are lists containing all
        elements that correspond to each key.

        :param key_selector: A function that takes an element of type T and returns a
        value of type Key to be used as the key.
        :return: A dictionary where each key is the result of applying the key selector
        function to the elements, and each value is a list of elements that share the
        same key.
        """
        return group_by(self._iterable, key_selector)

    def to_list(self) -> list[T]:
        """
        Converts the sequence into a list.

        :return: A list containing all elements of the sequence.
        """
        return list(self._iterable)

    def to_set(self) -> set[T]:
        """
        Converts the sequence into a set.

        :return: A set containing all elements of the sequence.
        """
        return set(self._iterable)

    def all(self, predicate: Optional[Callable[[T], bool]] = None) -> bool:
        """
        Checks if all elements in the sequence satisfy a specified condition.

        :param predicate: A function that evaluates each element in the sequence to a
        boolean value.
        :return: True if all elements satisfy the condition, False otherwise.
        """
        if predicate is None:
            return all(self._iterable)
        return all_by(self._iterable, predicate)

    def none(self, predicate: Optional[Callable[[T], bool]] = None) -> bool:
        """
        Checks if no elements in the sequence satisfy a specified condition.

        :param predicate: A function that evaluates each element in the sequence to a
        boolean value.
        :return: True if no elements satisfy the condition, False otherwise.
        """
        return not self.any(predicate)

    def any(self, predicate: Optional[Callable[[T], bool]] = None) -> bool:
        """
        Checks if any element in the sequence satisfies a specified condition.

        :param predicate: A function that evaluates each element in the sequence to a
        boolean value.
        :return: True if at least one element satisfies the condition, False otherwise.
        """
        if predicate is None:
            return any(self._iterable)
        return any_by(self._iterable, predicate)

    def max(self) -> T:
        """
        Returns the maximum element in the sequence.

        :return: The maximum element.
        :raises ValueError: If the sequence is empty.
        """
        return max(self._iterable)

    def max_or_none(self) -> Optional[T]:
        """
        Returns the maximum element in the sequence or None if the sequence is empty.

        :return: The maximum element or None if the sequence is empty.
        """
        return max_or_none(self._iterable)

    def max_by(self, selector: Callable[[T], R]) -> T:
        """
        Returns an element for which the given function returns the largest value.

        :param selector: A function that returns a comparable value for each element.
        :return: The element that gives the maximum value from the given function.
        :raises ValueError: If the sequence is empty.
        """
        return max_by(self._iterable, selector)

    def max_by_or_none(self, selector: Callable[[T], R]) -> Optional[T]:
        """
        Returns an element for which the given function returns the largest value or
        None if the sequence is empty.

        :param selector: A function that returns a comparable value for each element.
        :return: The element that gives the maximum value from the given function or
        None if the sequence is empty.
        """
        return max_by_or_none(self._iterable, selector)

    def min(self) -> T:
        """
        Returns the minimum element in the sequence.

        :return: The minimum element.
        :raises ValueError: If the sequence is empty.
        """
        return min(self._iterable)

    def min_or_none(self) -> Optional[T]:
        """
        Returns the minimum element in the sequence or None if the sequence is empty.

        :return: The minimum element or None if the sequence is empty.
        """
        return min_or_none(self)

    def min_by(self, selector: Callable[[T], R]) -> T:
        """
        Returns an element for which the given function returns the smallest value.

        :param selector: A function that returns a comparable value for each element.
        :return: The element that gives the smallest value from the given function.
        :raises ValueError: If the sequence is empty.
        """
        return min_by(self._iterable, selector)

    def min_by_or_none(self, selector: Callable[[T], R]) -> Optional[T]:
        """
        Returns an element for which the given function returns the smallest value or
        None if the sequence is empty.

        :param selector: A function that returns a comparable value for each element.
        :return: The element that gives the smallest value from the given function or
        None if the sequence is empty.
        """
        return min_by_or_none(self._iterable, selector)

    def single(self) -> T:
        """
        Returns the single element in the sequence.

        :return: The single element of the sequence.
        :raises ValueError: If the sequence is empty or contains more than one element.
        """
        return single(self._iterable)

    def single_or_none(self) -> Optional[T]:
        """
        Returns the single element in the sequence, or None if the sequence is empty or
        contains more than one element.

        :return: The single element of the sequence or None if the sequence is empty or
        contains more than one element.
        """
        return single_or_none(self._iterable)

    def first(self) -> T:
        """
        Returns the first element in the sequence.

        :return: The first element of the sequence.
        :raises ValueError: If the sequence is empty.
        """
        return first(self._iterable)

    def first_or_none(self) -> Optional[T]:
        """
        Returns the first element in the sequence, or None if the sequence is empty.

        :return: The first element of the sequence or None if the sequence is empty.
        """
        return first_or_none(self._iterable)

    def last(self) -> T:
        """
        Returns the last element in the sequence.

        :return: The last element of the sequence.
        :raises ValueError: If the sequence is empty.
        """
        return last(self._iterable)

    def last_or_none(self) -> Optional[T]:
        """
        Returns the first element in the sequence, or None if the sequence is empty.

        :return: The first element of the sequence or None if the sequence is empty.
        """
        return last_or_none(self._iterable)

    def drop(self, n: int) -> "Seq[T]":
        """
        Returns a new Seq skipping the first n elements of the original sequence.

        :param n: The number of elements to skip.
        :return: A new Seq instance with the first n elements dropped.
        """
        return drop(self._iterable, n)

    def drop_while(self, predicate: Callable[[T], bool]) -> "Seq[T]":
        """
        Returns a new Seq skipping the first elements as long as the predicate is true.

        :param predicate: A function that evaluates each element to a boolean.
        :return: A new Seq instance with the elements dropped as long as the predicate
        is true.
        """
        return drop_while(self._iterable, predicate)

    def take(self, n: int) -> "Seq[T]":
        """
        Returns a new Seq consisting of the first n elements of the original sequence.

        :param n: The number of elements to take.
        :return: A new Seq instance with at most n elements.
        """
        return take(self._iterable, n)

    def take_while(self, predicate: Callable[[T], bool]) -> "Seq[T]":
        """
        Returns a new Seq consisting of the elements of the original sequence as long as
        the predicate is true.

        :param predicate: A function that evaluates each element to a boolean.
        :return: A new Seq instance with elements as long as the predicate is true.
        """
        return take_while(self._iterable, predicate)

    def sorted(self) -> "Seq[T]":
        """
        Returns a new Seq with elements sorted in ascending order.

        :return: A new Seq instance with sorted elements.
        """
        return Seq(sorted(self._iterable))

    def sorted_by(self, key_func: Callable[[T], R]) -> "Seq[T]":
        """
        Returns a new Seq with elements sorted according to the specified key function.

        :param key_func: A function that extracts a comparison key from each element.
        :return: A new Seq instance with elements sorted by the key function.
        """
        return sorted_by(self._iterable, key_func)

    def sorted_desc(self) -> "Seq[T]":
        """
        Returns a new Seq with elements sorted in descending order.

        :return: A new Seq instance with elements sorted in descending order.
        """
        return sorted_desc(self._iterable)

    def sorted_by_desc(self, key_func: Callable[[T], R]) -> "Seq[T]":
        """
        Returns a new Seq with elements sorted in descending order according to the
        specified key function.

        :param key_func: A function that extracts a comparison key from each element.
        :return: A new Seq instance with elements sorted by the key function in
        descending order.
        """
        return sorted_by_desc(self._iterable, key_func)

    def chunked(self, size: int) -> "Seq[list[T]]":
        """
        Splits the sequence into chunks of the specified size.

        :param size: The size of each chunk.
        :return: A new Seq instance where each element is a list representing a chunk of
        the original sequence.
        """
        return chunked(self._iterable, size)

    def enumerate(self) -> "Seq[tuple[int, T]]":
        """
        Adds an index to each element of the sequence.

        :return: A new Seq instance where each element is a tuple (index, element).
        """
        return Seq(enumerate(self._iterable))

    def shuffled(self, rng: Optional[random.Random] = None) -> "Seq[T]":
        """
        Returns a new Seq with elements shuffled in random order.

        :param rng: An optional instance of random.Random for deterministic shuffling.
        If not provided, the default random generator is used, which is not
        deterministic.
        :return: A new Seq instance with randomly ordered elements.
        """
        return shuffled(self._iterable, rng)

    def reduce(self, operation: Callable[[T, T], T]) -> T:
        """
        Accumulates value starting with the first element and applying an operation from
        left to right to current
        accumulator value and each element.

        :param operation: A function that takes two arguments (accumulator, current
        element) and returns a new accumulator value.
        :return: The accumulated value.
        :raises TypeError: If the sequence is empty.
        """
        return reduce(self._iterable, operation)

    def reduce_or_none(self, operation: Callable[[T, T], T]) -> Optional[T]:
        """
        Accumulates value starting with the first element and applying an operation from
        left to right to current accumulator value and each element.

        :param operation: A function that takes two arguments (accumulator, current
        element) and returns a new accumulator value.
        :return: The accumulated value, or None if the sequence is empty.
        """
        return reduce_or_none(self._iterable, operation)

    def sum(self) -> T:
        """
        Returns the sum of all elements in the sequence.

        :return: The sum of the sequence elements.
        :raises TypeError: If the sequence is empty or contains non-numeric elements.
        """
        it = iter(self)
        try:
            first_value = next(it)
        except StopIteration:
            # pylint: disable=raise-missing-from
            raise TypeError("sum() called on an empty sequence")
        return sum(it, start=first_value)

    def sum_or_none(self) -> Optional[T]:
        """
        Calculates the sum of all elements in the sequence, or returns None if the
        sequence is empty.

        :return: The sum of the sequence elements, or None if the sequence is empty.
        """
        return sum_or_none(self._iterable)

    def distinct(self) -> "Seq[T]":
        """
        Returns a new Seq with distinct elements from the original sequence.

        :return: A new Seq instance with unique elements.
        """
        return distinct(self._iterable)

    def distinct_by(self, key_selector: Callable[[T], R]) -> "Seq[T]":
        """
        Returns a new Seq with elements that are distinct based on the key returned by
        the given keySelector function.

        :param key_selector: A function that returns a comparison key for each element.
        :return: A new Seq instance with distinct elements based on the key.
        """
        return distinct_by(self._iterable, key_selector)

    def for_each(self, action: Callable[[T], None]) -> None:
        """
        Performs the given action on each element of the sequence.

        :param action: A function that takes an element and performs an action.
        """
        for element in self._iterable:
            action(element)

    def join_to_string(
        self,
        separator: str = ", ",
        prefix: str = "",
        suffix: str = "",
    ) -> str:
        """
        Concatenates elements of the sequence into a single string with specified
        separators, prefix, and suffix.

        :param separator: The separator string to use between each element.
        :param prefix: The prefix string to add at the beginning.
        :param suffix: The suffix string to add at the end.
        :return: A string representation of the sequence elements.
        """
        return join_to_string(self._iterable, separator, prefix=prefix, suffix=suffix)

    def partition(self, predicate: Callable[[T], bool]) -> tuple["Seq[T]", "Seq[T]"]:
        """
        Splits the sequence into two sequences based on a predicate.

        :param predicate: The function to test each element of the sequence.
        :return: A tuple of two Seq instances: the first containing elements for which
        the predicate is True, and the second containing elements for which the
        predicate is False.
        """
        return partition(self._iterable, predicate)


def filter_not_none(sequence: Iterable[Optional[T]]) -> Seq[T]:
    """
    Filters out None values from the sequence.

    :param sequence: The sequence
    :return: A new Seq instance with all elements that are not None.
    """
    return Seq(d for d in sequence if d is not None)


def filter_is_instance(sequence: Iterable[T], cls: Type[R]) -> Seq[R]:
    """
    Filters elements of the sequence based on their type.

    :param sequence: The sequence
    :param cls: The class type to filter the elements by.
    :return: A new Seq instance containing only elements of the specified type.
    """
    return Seq((e for e in sequence if isinstance(e, cls)))


def map_not_none(sequence: Iterable[T], fn: Callable[[T], Optional[R]]) -> Seq[R]:
    """
    Applies a transformation function to each element in the sequence and filters
    out any "None" results.

    :param sequence: The sequence
    :param fn: A function that takes an element of type T and returns an Optional
    element of type R. The function is expected to return "None" for elements that
    should be filtered out.
    :return: A new Seq instance with transformed elements, excluding any "None"
    results.
    """
    return Seq(r for d in sequence if (r := fn(d)) is not None)


def flat_map(sequence: Iterable[T], fn: Callable[[T], Iterable[R]]) -> Seq[R]:
    """
    Applies a specified function to each element of the sequence that returns an
    iterable, and then flattens the result into a single sequence.

    :param sequence: The sequence
    :param fn: A function that takes an element of type T and returns an Iterable
    of type Iterable[R].
    :return: A new Seq instance containing all the elements from the iterables
    produced by applying the function to each element in the original sequence.
    """
    return Seq(jj for ii in (fn(d) for d in sequence) for jj in ii)


def flatten(sequence: Iterable[Iterable[R]]) -> Seq[R]:
    """
    Flattens a sequence of iterables into a single sequence.

    The elements of the sequence are expected to be iterables themselves. This
    method concatenates those iterables into a single sequence.

    :param sequence: The sequence
    :return: A new Seq instance containing all the elements of the inner iterables.
    """
    return Seq(jj for ii in sequence for jj in ii)


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
    return dict(fn(d) for d in sequence)


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
    return dict((key_selector(d), d) for d in sequence)


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
    return dict((d, value_selector(d)) for d in sequence)


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
    result = {}
    for d in sequence:
        result.setdefault(key_selector(d), []).append(d)
    return result


def all_by(sequence: Iterable[T], predicate: Callable[[T], bool]) -> bool:
    """
    Checks if all elements in the sequence satisfy a specified condition.

    :param sequence: The sequence
    :param predicate: A function that evaluates each element in the sequence to a
    boolean value.
    :return: True if all elements satisfy the condition, False otherwise.
    """
    return all(predicate(d) for d in sequence)


def none_by(sequence: Iterable[T], predicate: Callable[[T], bool]) -> bool:
    """
    Checks if no elements in the sequence satisfy a specified condition.

    :param sequence: The sequence
    :param predicate: A function that evaluates each element in the sequence to a
    boolean value.
    :return: True if no elements satisfy the condition, False otherwise.
    """
    return not any_by(sequence, predicate)


def any_by(sequence: Iterable[T], predicate: Callable[[T], bool]) -> bool:
    """
    Checks if any element in the sequence satisfies a specified condition.

    :param sequence: The sequence
    :param predicate: A function that evaluates each element in the sequence to a
    boolean value.
    :return: True if at least one element satisfies the condition, False otherwise.
    """
    return any(predicate(d) for d in sequence)


def max_or_none(sequence: Iterable[T]) -> Optional[T]:
    """
    Returns the maximum element in the sequence or None if the sequence is empty.

    :param sequence: The sequence
    :return: The maximum element or None if the sequence is empty.
    """
    try:
        return max(sequence)
    except ValueError:
        return None


def max_by(sequence: Iterable[T], selector: Callable[[T], R]) -> T:
    """
    Returns an element for which the given function returns the largest value.

    :param sequence: The sequence
    :param selector: A function that returns a comparable value for each element.
    :return: The element that gives the maximum value from the given function.
    :raises ValueError: If the sequence is empty.
    """
    return max(sequence, key=selector)


def max_by_or_none(sequence: Iterable[T], selector: Callable[[T], R]) -> Optional[T]:
    """
    Returns an element for which the given function returns the largest value or
    None if the sequence is empty.

    :param sequence: The sequence
    :param selector: A function that returns a comparable value for each element.
    :return: The element that gives the maximum value from the given function or
    None if the sequence is empty.
    """
    try:
        return max(sequence, key=selector)
    except ValueError:
        return None


def min_or_none(sequence: Iterable[T]) -> Optional[T]:
    """
    Returns the minimum element in the sequence or None if the sequence is empty.

    :param sequence: The sequence
    :return: The minimum element or None if the sequence is empty.
    """
    try:
        return min(sequence)
    except ValueError:
        return None


def min_by(sequence: Iterable[T], selector: Callable[[T], R]) -> T:
    """
    Returns an element for which the given function returns the smallest value.

    :param sequence: The sequence
    :param selector: A function that returns a comparable value for each element.
    :return: The element that gives the smallest value from the given function.
    :raises ValueError: If the sequence is empty.
    """
    return min(sequence, key=selector)


def min_by_or_none(sequence: Iterable[T], selector: Callable[[T], R]) -> Optional[T]:
    """
    Returns an element for which the given function returns the smallest value or
    None if the sequence is empty.

    :param sequence: The sequence
    :param selector: A function that returns a comparable value for each element.
    :return: The element that gives the smallest value from the given function or
    None if the sequence is empty.
    """
    try:
        return min(sequence, key=selector)
    except ValueError:
        return None


def single(sequence: Iterable[T]) -> T:
    """
    Returns the single element in the sequence.

    :param sequence: The sequence
    :return: The single element of the sequence.
    :raises ValueError: If the sequence is empty or contains more than one element.
    """
    it = iter(sequence)
    try:
        value = next(it)
    except StopIteration:
        # pylint: disable=raise-missing-from
        raise ValueError("single() called on an empty sequence")
    try:
        next(it)
        raise ValueError("single() called on a sequence with more than one element")
    except StopIteration:
        return value


def single_or_none(sequence: Iterable[T]) -> Optional[T]:
    """
    Returns the single element in the sequence, or None if the sequence is empty or
    contains more than one element.

    :param sequence: The sequence
    :return: The single element of the sequence or None if the sequence is empty or
    contains more than one element.
    """
    it = iter(sequence)
    try:
        value = next(it)
    except StopIteration:
        return None
    try:
        next(it)
        return None
    except StopIteration:
        return value


def first(sequence: Iterable[T]) -> T:
    """
    Returns the first element in the sequence.

    :param sequence: The sequence
    :return: The first element of the sequence.
    :raises ValueError: If the sequence is empty.
    """
    try:
        return next(iter(sequence))
    except StopIteration:
        # pylint: disable=raise-missing-from
        raise ValueError("first() called on an empty sequence")


def first_or_none(sequence: Iterable[T]) -> Optional[T]:
    """
    Returns the first element in the sequence, or None if the sequence is empty.

    :param sequence: The sequence
    :return: The first element of the sequence or None if the sequence is empty.
    """
    return next(iter(sequence), None)


def last(sequence: Iterable[T]) -> T:
    """
    Returns the last element in the sequence.

    :param sequence: The sequence
    :return: The last element of the sequence.
    :raises ValueError: If the sequence is empty.
    """
    if isinstance(sequence, (list, tuple, str)):
        if len(sequence) == 0:
            raise ValueError("last() called on an empty sequence")
        return sequence[-1]

    it = iter(sequence)
    try:
        last_value = next(it)
    except StopIteration:
        # pylint: disable=raise-missing-from
        raise ValueError("last() called on an empty sequence")
    for x in it:
        last_value = x
    return last_value


def last_or_none(sequence: Iterable[T]) -> Optional[T]:
    """
    Returns the first element in the sequence, or None if the sequence is empty.

    :param sequence: The sequence
    :return: The first element of the sequence or None if the sequence is empty.
    """
    if isinstance(sequence, (list, tuple, str)):
        if len(sequence) == 0:
            return None
        return sequence[-1]

    last_value = None
    for x in sequence:
        last_value = x
    return last_value


def drop(sequence: Iterable[T], n: int) -> Seq[T]:
    """
    Returns a new Seq skipping the first n elements of the original sequence.

    :param sequence: The sequence
    :param n: The number of elements to skip.
    :return: A new Seq instance with the first n elements dropped.
    """
    return Seq(x for i, x in enumerate(sequence) if i >= n)


def drop_while(sequence: Iterable[T], predicate: Callable[[T], bool]) -> Seq[T]:
    """
    Returns a new Seq skipping the first elements as long as the predicate is true.

    :param sequence: The sequence
    :param predicate: A function that evaluates each element to a boolean.
    :return: A new Seq instance with the elements dropped as long as the predicate
    is true.
    """

    def generator():
        iterator = iter(sequence)
        for element in iterator:
            if not predicate(element):
                yield element
                break
        for element in iterator:
            yield element

    return Seq(generator())


def take(sequence: Iterable[T], n: int) -> Seq[T]:
    """
    Returns a new Seq consisting of the first n elements of the original sequence.

    :param sequence: The sequence
    :param n: The number of elements to take.
    :return: A new Seq instance with at most n elements.
    """
    return Seq(item for i, item in enumerate(sequence) if i < n)


def take_while(sequence: Iterable[T], predicate: Callable[[T], bool]) -> Seq[T]:
    """
    Returns a new Seq consisting of the elements of the original sequence as long as
    the predicate is true.

    :param sequence: The sequence
    :param predicate: A function that evaluates each element to a boolean.
    :return: A new Seq instance with elements as long as the predicate is true.
    """

    def generator():
        for element in sequence:
            if predicate(element):
                yield element
            else:
                break

    return Seq(generator())


def sorted_by(sequence: Iterable[T], key_func: Callable[[T], R]) -> Seq[T]:
    """
    Returns a new Seq with elements sorted according to the specified key function.

    :param sequence: The sequence
    :param key_func: A function that extracts a comparison key from each element.
    :return: A new Seq instance with elements sorted by the key function.
    """
    return Seq(sorted(sequence, key=key_func))


def sorted_desc(sequence: Iterable[T]) -> Seq[T]:
    """
    Returns a new Seq with elements sorted in descending order.

    :param sequence: The sequence
    :return: A new Seq instance with elements sorted in descending order.
    """
    return Seq(sorted(sequence, reverse=True))


def sorted_by_desc(sequence: Iterable[T], key_func: Callable[[T], R]) -> Seq[T]:
    """
    Returns a new Seq with elements sorted in descending order according to the
    specified key function.

    :param sequence: The sequence
    :param key_func: A function that extracts a comparison key from each element.
    :return: A new Seq instance with elements sorted by the key function in
    descending order.
    """
    return Seq(sorted(sequence, key=key_func, reverse=True))


def chunked(sequence: Iterable[T], size: int) -> Seq[list[T]]:
    """
    Splits the sequence into chunks of the specified size.

    :param sequence: The sequence
    :param size: The size of each chunk.
    :return: A new Seq instance where each element is a list representing a chunk of
    the original sequence.
    """

    def generator():
        it = iter(sequence)
        while True:
            chunk = list(islice(it, size))
            if not chunk:
                break
            yield chunk

    return Seq(generator())


def shuffled(sequence: Iterable[T], rng: Optional[random.Random] = None) -> Seq[T]:
    """
    Returns a new Seq with elements shuffled in random order.

    :param sequence: The sequence
    :param rng: An optional instance of random.Random for deterministic shuffling.
    If not provided, the default random generator is used, which is not
    deterministic.
    :return: A new Seq instance with randomly ordered elements.
    """
    elements = list(sequence)  # Convert to list to shuffle
    if rng is None:
        random.shuffle(elements)
    else:
        rng.shuffle(elements)
    return Seq(elements)


def reduce(sequence: Iterable[T], operation: Callable[[T, T], T]) -> T:
    """
    Accumulates value starting with the first element and applying an operation from
    left to right to current
    accumulator value and each element.

    :param sequence: The sequence
    :param operation: A function that takes two arguments (accumulator, current
    element) and returns a new accumulator value.
    :return: The accumulated value.
    :raises TypeError: If the sequence is empty.
    """
    it = iter(sequence)
    try:
        accumulator = next(it)
    except StopIteration:
        # pylint: disable=raise-missing-from
        raise TypeError("reduce() of empty sequence with no initial value")
    for element in it:
        accumulator = operation(accumulator, element)
    return accumulator


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
    it = iter(sequence)
    try:
        accumulator = next(it)
    except StopIteration:
        return None
    for element in it:
        accumulator = operation(accumulator, element)
    return accumulator


def sum_or_none(sequence: Iterable[T]) -> Optional[T]:
    """
    Calculates the sum of all elements in the sequence, or returns None if the
    sequence is empty.

    :param sequence: The sequence
    :return: The sum of the sequence elements, or None if the sequence is empty.
    """
    it = iter(sequence)
    try:
        first_value = next(it)
    except StopIteration:
        return None
    return sum(it, start=first_value)


def distinct(sequence: Iterable[T]) -> Seq[T]:
    """
    Returns a new Seq with distinct elements from the original sequence.

    :param sequence: The sequence
    :return: A new Seq instance with unique elements.
    """
    seen = set()

    def check_key(key) -> bool:
        if key in seen:
            return False
        seen.add(key)
        return True

    return Seq(x for x in sequence if check_key(x))


def distinct_by(sequence: Iterable[T], key_selector: Callable[[T], R]) -> Seq[T]:
    """
    Returns a new Seq with elements that are distinct based on the key returned by
    the given keySelector function.

    :param sequence: The sequence
    :param key_selector: A function that returns a comparison key for each element.
    :return: A new Seq instance with distinct elements based on the key.
    """
    seen = set()

    def check_key(key) -> bool:
        if key in seen:
            return False
        seen.add(key)
        return True

    return Seq(e for e in sequence if check_key(key_selector(e)))


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
    return prefix + separator.join(str(e) for e in sequence) + suffix


def partition(
    sequence: Iterable[T], predicate: Callable[[T], bool]
) -> tuple[Seq[T], Seq[T]]:
    """
    Splits the sequence into two sequences based on a predicate.

    :param sequence: The sequence
    :param predicate: The function to test each element of the sequence.
    :return: A tuple of two Seq instances: the first containing elements for which
    the predicate is True, and the second containing elements for which the
    predicate is False.
    """
    true_seq, false_seq = [], []
    for element in sequence:
        if predicate(element):
            true_seq.append(element)
        else:
            false_seq.append(element)
    return Seq(true_seq), Seq(false_seq)
