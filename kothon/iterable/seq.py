"""
This script demonstrates the usage of the Seq class for performing a series of
transformations and operations on sequences of data. The Seq class provides a
lazy-evaluation mechanism for efficiently chaining operations such as mapping,
filtering, and reducing sequences.
"""

import functools
import operator
import random
from itertools import islice
from typing import Generic, Iterator, TypeVar, Iterable, Callable, Optional, Type

from .._utils.type_utils import CT, AT

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
        return Seq(filter(predicate, self))

    def filter_not_none(self: "Seq[Optional[R]]") -> "Seq[R]":
        """
        Filters out None values from the sequence.

        :return: A new Seq instance with all elements that are not None.
        """
        return Seq(d for d in self if d is not None)

    def filter_is_instance(self, cls: Type[R]) -> "Seq[R]":
        """
        Filters elements of the sequence based on their type.

        :param cls: The class type to filter the elements by.
        :return: A new Seq instance containing only elements of the specified type.
        """
        return Seq(e for e in self if isinstance(e, cls))

    def map(self, fn: Callable[[T], R]) -> "Seq[R]":
        """
        Transforms each element in the sequence using a given function.

        :param fn: A function that takes an element of type T and returns an element of
        type R.
        :return: A new Seq instance with transformed elements.
        """
        return Seq(map(fn, self))

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
        return Seq(r for d in self if (r := fn(d)) is not None)

    def flat_map(self, fn: Callable[[T], Iterable[R]]) -> "Seq[R]":
        """
        Applies a specified function to each element of the sequence that returns an
        iterable, and then flattens the result into a single sequence.

        :param fn: A function that takes an element of type T and returns an Iterable
        of type Iterable[R].
        :return: A new Seq instance containing all the elements from the iterables
        produced by applying the function to each element in the original sequence.
        """
        return Seq(jj for ii in (fn(d) for d in self) for jj in ii)

    def flatten(self: "Seq[Iterable[R]]") -> "Seq[R]":
        """
        Flattens a sequence of iterables into a single sequence.

        The elements of the sequence are expected to be iterables themselves. This
        method concatenates those iterables into a single sequence.

        :return: A new Seq instance containing all the elements of the inner iterables.
        """
        return Seq(jj for ii in self for jj in ii)

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
        return dict(fn(d) for d in self)

    def associate_by(self, key_selector: Callable[[T], Key]) -> dict[Key, T]:
        """
        Creates a dictionary from the sequence by determining the keys using a specified
        key selector function. The values in the dictionary are the elements themselves.

        :param key_selector: A function that takes an element of type T and returns a
        value of type Key that will be used as the key.
        :return: A dictionary where each key is the result of applying the key selector
        function to each element, and each value is the element itself.
        """
        return dict((key_selector(d), d) for d in self)

    def associate_with(self, value_selector: Callable[[T], Value]) -> dict[T, Value]:
        """
        Creates a dictionary from the sequence with elements as keys and values
        determined by a specified value selector function.

        :param value_selector: A function that takes an element of type T and returns a
        value of type Value to be associated with the key.
        :return: A dictionary where each key is an element from the sequence, and each
        value is the result of applying the value selector function to that element.
        """
        return dict((d, value_selector(d)) for d in self)

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
        result: dict[Key, list[T]] = {}
        for d in self:
            result.setdefault(key_selector(d), []).append(d)
        return result

    def to_list(self) -> list[T]:
        """
        Converts the sequence into a list.

        :return: A list containing all elements of the sequence.
        """
        return list(self)

    def to_set(self) -> set[T]:
        """
        Converts the sequence into a set.

        :return: A set containing all elements of the sequence.
        """
        return set(self)

    def to_frozenset(self) -> frozenset[T]:
        """
        Converts the sequence into a frozenset.

        :return: A set containing all elements of the sequence.
        """
        return frozenset(self)

    def all(self, predicate: Optional[Callable[[T], bool]] = None) -> bool:
        """
        Checks if all elements in the sequence satisfy a specified condition.

        :param predicate: A function that evaluates each element in the sequence to a
        boolean value.
        :return: True if all elements satisfy the condition, False otherwise.
        """
        if predicate is None:
            return all(self)
        return all(predicate(d) for d in self)

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
            return any(self)
        return any(predicate(d) for d in self)

    def max(self: "Seq[CT]") -> CT:
        """
        Returns the maximum element in the sequence.

        :return: The maximum element.
        :raises ValueError: If the sequence is empty.
        """
        return max(self)

    def max_or_none(self: "Seq[CT]") -> Optional[CT]:
        """
        Returns the maximum element in the sequence or None if the sequence is empty.

        :return: The maximum element or None if the sequence is empty.
        """
        return self.reduce_or_none(max)

    def max_by(self, selector: Callable[[T], CT]) -> T:
        """
        Returns an element for which the given function returns the largest value.

        :param selector: A function that returns a comparable value for each element.
        :return: The element that gives the maximum value from the given function.
        :raises ValueError: If the sequence is empty.
        """
        return max(self, key=selector)

    def max_by_or_none(self, selector: Callable[[T], CT]) -> Optional[T]:
        """
        Returns an element for which the given function returns the largest value or
        None if the sequence is empty.

        :param selector: A function that returns a comparable value for each element.
        :return: The element that gives the maximum value from the given function or
        None if the sequence is empty.
        """
        result: Optional[tuple[CT, T]] = Seq(
            (selector(v), v) for v in self
        ).reduce_or_none(lambda x, y: x if x[0] > y[0] else y)
        if result is not None:
            return result[1]
        return None

    def min(self: "Seq[CT]") -> CT:
        """
        Returns the minimum element in the sequence.

        :return: The minimum element.
        :raises ValueError: If the sequence is empty.
        """
        return min(self)

    def min_or_none(self: "Seq[CT]") -> Optional[CT]:
        """
        Returns the minimum element in the sequence or None if the sequence is empty.

        :return: The minimum element or None if the sequence is empty.
        """
        return self.reduce_or_none(min)

    def min_by(self, selector: Callable[[T], CT]) -> T:
        """
        Returns an element for which the given function returns the smallest value.

        :param selector: A function that returns a comparable value for each element.
        :return: The element that gives the smallest value from the given function.
        :raises ValueError: If the sequence is empty.
        """
        return min(self, key=selector)

    def min_by_or_none(self, selector: Callable[[T], CT]) -> Optional[T]:
        """
        Returns an element for which the given function returns the smallest value or
        None if the sequence is empty.

        :param selector: A function that returns a comparable value for each element.
        :return: The element that gives the smallest value from the given function or
        None if the sequence is empty.
        """
        result: Optional[tuple[CT, T]] = Seq(
            (selector(v), v) for v in self
        ).reduce_or_none(lambda x, y: x if x[0] < y[0] else y)
        if result is not None:
            return result[1]
        return None

    def single(self) -> T:
        """
        Returns the single element in the sequence.

        :return: The single element of the sequence.
        :raises ValueError: If the sequence is empty or contains more than one element.
        """
        it = iter(self)
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

    def single_or_none(self) -> Optional[T]:
        """
        Returns the single element in the sequence, or None if the sequence is empty or
        contains more than one element.

        :return: The single element of the sequence or None if the sequence is empty or
        contains more than one element.
        """
        it = iter(self)
        try:
            value = next(it)
        except StopIteration:
            return None
        try:
            next(it)
            return None
        except StopIteration:
            return value

    def first(self) -> T:
        """
        Returns the first element in the sequence.

        :return: The first element of the sequence.
        :raises ValueError: If the sequence is empty.
        """
        try:
            return next(iter(self))
        except StopIteration:
            # pylint: disable=raise-missing-from
            raise ValueError("first() called on an empty sequence")

    def first_or_none(self) -> Optional[T]:
        """
        Returns the first element in the sequence, or None if the sequence is empty.

        :return: The first element of the sequence or None if the sequence is empty.
        """
        return next(iter(self), None)

    def last(self) -> T:
        """
        Returns the last element in the sequence.

        :return: The last element of the sequence.
        :raises ValueError: If the sequence is empty.
        """
        if isinstance(self._iterable, (list, tuple, str)):
            if len(self._iterable) == 0:
                raise ValueError("last() called on an empty sequence")
            result: T = self._iterable[-1]
            return result

        it = iter(self)
        try:
            last_value = next(it)
        except StopIteration:
            # pylint: disable=raise-missing-from
            raise ValueError("last() called on an empty sequence")
        for x in it:
            last_value = x
        return last_value

    def last_or_none(self) -> Optional[T]:
        """
        Returns the first element in the sequence, or None if the sequence is empty.

        :return: The first element of the sequence or None if the sequence is empty.
        """
        if isinstance(self._iterable, (list, tuple, str)):
            if len(self._iterable) == 0:
                return None
            result: T = self._iterable[-1]
            return result

        last_value = None
        for x in self:
            last_value = x
        return last_value

    def drop(self, n: int) -> "Seq[T]":
        """
        Returns a new Seq skipping the first n elements of the original sequence.

        :param n: The number of elements to skip.
        :return: A new Seq instance with the first n elements dropped.
        """
        return Seq(x for i, x in enumerate(self) if i >= n)

    def drop_while(self, predicate: Callable[[T], bool]) -> "Seq[T]":
        """
        Returns a new Seq skipping the first elements as long as the predicate is true.

        :param predicate: A function that evaluates each element to a boolean.
        :return: A new Seq instance with the elements dropped as long as the predicate
        is true.
        """

        def generator() -> Iterable[T]:
            iterator = iter(self)
            for element in iterator:
                if not predicate(element):
                    yield element
                    break
            yield from iterator

        return Seq(generator())

    def take(self, n: int) -> "Seq[T]":
        """
        Returns a new Seq consisting of the first n elements of the original sequence.

        :param n: The number of elements to take.
        :return: A new Seq instance with at most n elements.
        """
        return Seq(item for i, item in enumerate(self) if i < n)

    def take_while(self, predicate: Callable[[T], bool]) -> "Seq[T]":
        """
        Returns a new Seq consisting of the elements of the original sequence as long as
        the predicate is true.

        :param predicate: A function that evaluates each element to a boolean.
        :return: A new Seq instance with elements as long as the predicate is true.
        """

        def generator() -> Iterable[T]:
            for element in self:
                if predicate(element):
                    yield element
                else:
                    break

        return Seq(generator())

    def sorted(self: "Seq[CT]") -> "Seq[CT]":
        """
        Returns a new Seq with elements sorted in ascending order.

        :return: A new Seq instance with sorted elements.
        """
        return Seq(sorted(self))

    def sorted_by(self, key_func: Callable[[T], CT]) -> "Seq[T]":
        """
        Returns a new Seq with elements sorted according to the specified key function.

        :param key_func: A function that extracts a comparison key from each element.
        :return: A new Seq instance with elements sorted by the key function.
        """
        return Seq(sorted(self, key=key_func))

    def sorted_desc(self: "Seq[CT]") -> "Seq[CT]":
        """
        Returns a new Seq with elements sorted in descending order.

        :return: A new Seq instance with elements sorted in descending order.
        """
        return Seq(sorted(self, reverse=True))

    def sorted_by_desc(self, key_func: Callable[[T], CT]) -> "Seq[T]":
        """
        Returns a new Seq with elements sorted in descending order according to the
        specified key function.

        :param key_func: A function that extracts a comparison key from each element.
        :return: A new Seq instance with elements sorted by the key function in
        descending order.
        """
        return Seq(sorted(self, key=key_func, reverse=True))

    def chunked(self, size: int) -> "Seq[list[T]]":
        """
        Splits the sequence into chunks of the specified size.

        :param size: The size of each chunk.
        :return: A new Seq instance where each element is a list representing a chunk of
        the original sequence.
        """
        if size < 1:
            raise ValueError("size must be greater than 0")

        def generator() -> Iterable[list[T]]:
            it = iter(self)
            while True:
                chunk = list(islice(it, size))
                if not chunk:
                    break
                yield chunk

        return Seq(generator())

    def enumerate(self) -> "Seq[tuple[int, T]]":
        """
        Adds an index to each element of the sequence.

        :return: A new Seq instance where each element is a tuple (index, element).
        """
        return Seq(enumerate(self))

    def shuffled(self, rng: Optional[random.Random] = None) -> "Seq[T]":
        """
        Returns a new Seq with elements shuffled in random order.

        :param rng: An optional instance of random.Random for deterministic shuffling.
        If not provided, the default random generator is used, which is not
        deterministic.
        :return: A new Seq instance with randomly ordered elements.
        """
        elements = list(self)
        if rng is None:
            random.shuffle(elements)
        else:
            rng.shuffle(elements)
        return Seq(elements)

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
        return functools.reduce(operation, self)

    def reduce_or_none(self, operation: Callable[[T, T], T]) -> Optional[T]:
        """
        Accumulates value starting with the first element and applying an operation from
        left to right to current accumulator value and each element.

        :param operation: A function that takes two arguments (accumulator, current
        element) and returns a new accumulator value.
        :return: The accumulated value, or None if the sequence is empty.
        """
        it = iter(self)
        try:
            accumulator: T = next(it)
        except StopIteration:
            return None
        for element in it:
            accumulator = operation(accumulator, element)
        return accumulator

    def sum(self: "Seq[AT]") -> AT:
        """
        Returns the sum of all elements in the sequence.

        :return: The sum of the sequence elements.
        :raises TypeError: If the sequence is empty or contains non-numeric elements.
        """
        return self.reduce(operator.add)

    def sum_or_none(self: "Seq[AT]") -> Optional[AT]:
        """
        Calculates the sum of all elements in the sequence, or returns None if the
        sequence is empty.

        :return: The sum of the sequence elements, or None if the sequence is empty.
        """
        return self.reduce_or_none(operator.add)

    def distinct(self) -> "Seq[T]":
        """
        Returns a new Seq with distinct elements from the original sequence.

        :return: A new Seq instance with unique elements.
        """
        seen: set[T] = set()

        def check_key(key: T) -> bool:
            if key in seen:
                return False
            seen.add(key)
            return True

        return Seq(x for x in self if check_key(x))

    def distinct_by(self, key_selector: Callable[[T], R]) -> "Seq[T]":
        """
        Returns a new Seq with elements that are distinct based on the key returned by
        the given keySelector function.

        :param key_selector: A function that returns a comparison key for each element.
        :return: A new Seq instance with distinct elements based on the key.
        """
        seen: set[R] = set()

        def check_key(key: R) -> bool:
            if key in seen:
                return False
            seen.add(key)
            return True

        return Seq(e for e in self if check_key(key_selector(e)))

    def for_each(self, action: Callable[[T], None]) -> None:
        """
        Performs the given action on each element of the sequence.

        :param action: A function that takes an element and performs an action.
        """
        for element in self:
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
        return prefix + separator.join(str(e) for e in self) + suffix

    def partition(self, predicate: Callable[[T], bool]) -> tuple[list[T], list[T]]:
        """
        Splits the sequence into two sequences based on a predicate.

        :param predicate: The function to test each element of the sequence.
        :return: A tuple of two Seq instances: the first containing elements for which
        the predicate is True, and the second containing elements for which the
        predicate is False.
        """
        true_seq, false_seq = [], []
        for element in self:
            if predicate(element):
                true_seq.append(element)
            else:
                false_seq.append(element)
        return true_seq, false_seq
