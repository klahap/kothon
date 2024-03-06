"""kothon sequence functions"""

import random
from typing import Iterable, Optional, TypeVar, Type, Callable

from .._utils.type_utils import CT
from ..iterable.seq import Seq

T = TypeVar("T")
R = TypeVar("R")


def filter_not_none(sequence: Iterable[Optional[T]]) -> Seq[T]:
    """
    Filters out None values from the sequence.

    :param sequence: The sequence
    :return: A new Seq instance with all elements that are not None.
    """
    return Seq(sequence).filter_not_none()


def filter_is_instance(sequence: Iterable[T], cls: Type[R]) -> Seq[R]:
    """
    Filters elements of the sequence based on their type.

    :param sequence: The sequence
    :param cls: The class type to filter the elements by.
    :return: A new Seq instance containing only elements of the specified type.
    """
    return Seq(sequence).filter_is_instance(cls)


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
    return Seq(sequence).map_not_none(fn)


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
    return Seq(sequence).flat_map(fn)


def flatten(sequence: Iterable[Iterable[R]]) -> Seq[R]:
    """
    Flattens a sequence of iterables into a single sequence.

    The elements of the sequence are expected to be iterables themselves. This
    method concatenates those iterables into a single sequence.

    :param sequence: The sequence
    :return: A new Seq instance containing all the elements of the inner iterables.
    """
    return Seq(sequence).flatten()


def drop(sequence: Iterable[T], n: int) -> Seq[T]:
    """
    Returns a new Seq skipping the first n elements of the original sequence.

    :param sequence: The sequence
    :param n: The number of elements to skip.
    :return: A new Seq instance with the first n elements dropped.
    """
    return Seq(sequence).drop(n)


def drop_while(sequence: Iterable[T], predicate: Callable[[T], bool]) -> Seq[T]:
    """
    Returns a new Seq skipping the first elements as long as the predicate is true.

    :param sequence: The sequence
    :param predicate: A function that evaluates each element to a boolean.
    :return: A new Seq instance with the elements dropped as long as the predicate
    is true.
    """
    return Seq(sequence).drop_while(predicate)


def take(sequence: Iterable[T], n: int) -> Seq[T]:
    """
    Returns a new Seq consisting of the first n elements of the original sequence.

    :param sequence: The sequence
    :param n: The number of elements to take.
    :return: A new Seq instance with at most n elements.
    """
    return Seq(sequence).take(n)


def take_while(sequence: Iterable[T], predicate: Callable[[T], bool]) -> Seq[T]:
    """
    Returns a new Seq consisting of the elements of the original sequence as long as
    the predicate is true.

    :param sequence: The sequence
    :param predicate: A function that evaluates each element to a boolean.
    :return: A new Seq instance with elements as long as the predicate is true.
    """
    return Seq(sequence).take_while(predicate)


def sorted_by(sequence: Iterable[T], key_func: Callable[[T], CT]) -> Seq[T]:
    """
    Returns a new Seq with elements sorted according to the specified key function.

    :param sequence: The sequence
    :param key_func: A function that extracts a comparison key from each element.
    :return: A new Seq instance with elements sorted by the key function.
    """
    return Seq(sequence).sorted_by(key_func)


def sorted_desc(sequence: Iterable[CT]) -> Seq[CT]:
    """
    Returns a new Seq with elements sorted in descending order.

    :param sequence: The sequence
    :return: A new Seq instance with elements sorted in descending order.
    """
    return Seq(sequence).sorted_desc()


def sorted_by_desc(sequence: Iterable[T], key_func: Callable[[T], CT]) -> Seq[T]:
    """
    Returns a new Seq with elements sorted in descending order according to the
    specified key function.

    :param sequence: The sequence
    :param key_func: A function that extracts a comparison key from each element.
    :return: A new Seq instance with elements sorted by the key function in
    descending order.
    """
    return Seq(sequence).sorted_by_desc(key_func)


def chunked(sequence: Iterable[T], size: int) -> Seq[list[T]]:
    """
    Splits the sequence into chunks of the specified size.

    :param sequence: The sequence
    :param size: The size of each chunk.
    :return: A new Seq instance where each element is a list representing a chunk of
    the original sequence.
    """
    return Seq(sequence).chunked(size)


def shuffled(sequence: Iterable[T], rng: Optional[random.Random] = None) -> Seq[T]:
    """
    Returns a new Seq with elements shuffled in random order.

    :param sequence: The sequence
    :param rng: An optional instance of random.Random for deterministic shuffling.
    If not provided, the default random generator is used, which is not
    deterministic.
    :return: A new Seq instance with randomly ordered elements.
    """
    return Seq(sequence).shuffled(rng)


def distinct(sequence: Iterable[T]) -> Seq[T]:
    """
    Returns a new Seq with distinct elements from the original sequence.

    :param sequence: The sequence
    :return: A new Seq instance with unique elements.
    """
    return Seq(sequence).distinct()


def distinct_by(sequence: Iterable[T], key_selector: Callable[[T], R]) -> Seq[T]:
    """
    Returns a new Seq with elements that are distinct based on the key returned by
    the given keySelector function.

    :param sequence: The sequence
    :param key_selector: A function that returns a comparison key for each element.
    :return: A new Seq instance with distinct elements based on the key.
    """
    return Seq(sequence).distinct_by(key_selector)


def partition(
    sequence: Iterable[T], predicate: Callable[[T], bool]
) -> tuple[list[T], list[T]]:
    """
    Splits the sequence into two sequences based on a predicate.

    :param sequence: The sequence
    :param predicate: The function to test each element of the sequence.
    :return: A tuple of two Seq instances: the first containing elements for which
    the predicate is True, and the second containing elements for which the
    predicate is False.
    """
    return Seq(sequence).partition(predicate)
