"""kothon sequence functions"""

from typing import Iterable, Optional, TypeVar, Type, Callable, overload, Union

from .._utils.type_utils import CT
from ..iterable.seq import Seq

T = TypeVar("T")
R = TypeVar("R")


def kothon_filter(predicate: Callable[[T], bool]) -> Callable[[Iterable[T]], Seq[T]]:
    """
    Builds a function that filters elements in the sequence based on a predicate.

    :param predicate: A function that evaluates each element to a boolean.
    :return: Function that filters elements in the sequence based on a predicate.
    """
    return lambda s: Seq(filter(predicate, s))


def filter_not_none(sequence: Iterable[Optional[T]]) -> Seq[T]:
    """
    Filters out None values from the sequence.

    :param sequence: The sequence
    :return: A new Seq instance with all elements that are not None.
    """
    return Seq(sequence).filter_not_none()


@overload
def filter_is_instance(
    cls: Type[R],
    sequence: Iterable[T],
) -> Seq[R]:
    """
    Filters elements of the sequence based on their type.

    :param cls: The class type to filter the elements by.
    :param sequence: The sequence.
    :return: A new Seq instance containing only elements of the specified type.
    """


@overload
def filter_is_instance(cls: Type[R]) -> Callable[[Iterable[T]], Seq[R]]:
    """
    Builds a function that filters elements of a sequence based on their type.

    :param cls: The class type to filter the elements by.
    :return: Function that filters elements of a sequence based on their type.
    """


def filter_is_instance(
    cls: Type[R],
    sequence: Optional[Iterable[T]] = None,
) -> Union[Seq[R], Callable[[Iterable[T]], Seq[R]]]:
    """
    Filters elements of the sequence based on their type.

    :param cls: The class type to filter the elements by.
    :param sequence: The sequence. If None, a callable is returned.
    :return: A new Seq instance containing only elements of the specified type.
    """
    if sequence is None:
        return lambda s: Seq(s).filter_is_instance(cls)
    return Seq(sequence).filter_is_instance(cls)


def kothon_map(fn: Callable[[T], R]) -> Callable[[Iterable[T]], Seq[R]]:
    """
    Builds a function that transforms each element in the sequence using a given
    function fn.

    :param fn: A function that takes an element of type T and returns an element of
    type R.
    :return: Function that transforms each element in the sequence using a given
    function fn.
    """
    return lambda s: Seq(map(fn, s))


@overload
def map_not_none(
    fn: Callable[[T], Optional[R]],
    sequence: Iterable[T],
) -> Seq[R]:
    """
    Applies a transformation function to each element in the sequence and filters
    out any "None" results.

    :param fn: A function that takes an element of type T and returns an Optional
    element of type R. The function is expected to return "None" for elements that
    should be filtered out.
    :param sequence: The sequence
    :return: A new Seq instance with transformed elements, excluding any "None"
    results.
    """


@overload
def map_not_none(
    fn: Callable[[T], Optional[R]],
) -> Callable[[Iterable[T]], Seq[R]]:
    """
    Builds a function that applies a transformation function to each element in the
    sequence and filters out any "None" results.

    :param fn: A function that takes an element of type T and returns an Optional
    element of type R. The function is expected to return "None" for elements that
    should be filtered out.
    :return: Function that applies a transformation function to each element in the
    sequence and filters out any "None" results.
    """


def map_not_none(
    fn: Callable[[T], Optional[R]],
    sequence: Optional[Iterable[T]] = None,
) -> Union[Seq[R], Callable[[Iterable[T]], Seq[R]]]:
    """
    Applies a transformation function to each element in the sequence and filters
    out any "None" results.

    :param fn: A function that takes an element of type T and returns an Optional
    element of type R. The function is expected to return "None" for elements that
    should be filtered out.
    :param sequence: The sequence. If None, a callable is returned.
    :return: A new Seq instance with transformed elements, excluding any "None"
    results.
    """
    if sequence is None:
        return lambda s: Seq(s).map_not_none(fn)
    return Seq(sequence).map_not_none(fn)


@overload
def flat_map(
    fn: Callable[[T], Iterable[R]],
    sequence: Iterable[T],
) -> Seq[R]:
    """
    Applies a specified function to each element of the sequence that returns an
    iterable, and then flattens the result into a single sequence.

    :param fn: A function that takes an element of type T and returns an Iterable
    of type Iterable[R].
    :param sequence: The sequence.
    :return: A new Seq instance containing all the elements from the iterables
    produced by applying the function to each element in the original sequence.
    """


@overload
def flat_map(fn: Callable[[T], Iterable[R]]) -> Callable[[Iterable[T]], Seq[R]]:
    """
    Builds a function that applies a specified function to each element of the sequence
    that returns an iterable, and then flattens the result into a single sequence.

    :param fn: A function that takes an element of type T and returns an Iterable
    of type Iterable[R].
    :return: Function that applies a specified function to each element of the sequence
    that returns an iterable, and then flattens the result into a single sequence.
    """


def flat_map(
    fn: Callable[[T], Iterable[R]],
    sequence: Optional[Iterable[T]] = None,
) -> Union[Seq[R], Callable[[Iterable[T]], Seq[R]]]:
    """
    Applies a specified function to each element of the sequence that returns an
    iterable, and then flattens the result into a single sequence.

    :param fn: A function that takes an element of type T and returns an Iterable
    of type Iterable[R].
    :param sequence: The sequence.
    :return: A new Seq instance containing all the elements from the iterables
    produced by applying the function to each element in the original sequence.
    """
    if sequence is None:
        return lambda s: Seq(s).flat_map(fn)
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


@overload
def drop(
    n: int,
    sequence: Iterable[T],
) -> Seq[T]:
    """
    Returns a new Seq skipping the first n elements of the original sequence.

    :param n: The number of elements to skip.
    :param sequence: The sequence
    :return: A new Seq instance with the first n elements dropped.
    """


@overload
def drop(n: int) -> Callable[[Iterable[T]], Seq[T]]:
    """
    Builds a function that returns a new Seq skipping the first n elements of the
    original sequence.

    :param n: The number of elements to skip.
    :return: Function that returns a new Seq skipping the first n elements of the
    original sequence.
    """


def drop(
    n: int,
    sequence: Optional[Iterable[T]] = None,
) -> Union[Seq[T], Callable[[Iterable[T]], Seq[T]]]:
    """
    Returns a new Seq skipping the first n elements of the original sequence.

    :param n: The number of elements to skip.
    :param sequence: The sequence. If None, a callable is returned.
    :return: A new Seq instance with the first n elements dropped.
    """
    if sequence is None:
        return lambda s: Seq(s).drop(n)
    return Seq(sequence).drop(n)


@overload
def drop_while(
    predicate: Callable[[T], bool],
    sequence: Iterable[T],
) -> Seq[T]:
    """
    Returns a new Seq skipping the first elements as long as the predicate is true.

    :param predicate: A function that evaluates each element to a boolean.
    :param sequence: The sequence
    :return: A new Seq instance with the elements dropped as long as the predicate
    is true.
    """


@overload
def drop_while(
    predicate: Callable[[T], bool],
) -> Callable[[Iterable[T]], Seq[T]]:
    """
    Builds a function that returns a new Seq skipping the first elements as long as the
    predicate is true.

    :param predicate: A function that evaluates each element to a boolean.
    :return: Function that returns a new Seq skipping the first elements as long as the
    predicate is true.
    """


def drop_while(
    predicate: Callable[[T], bool],
    sequence: Optional[Iterable[T]] = None,
) -> Union[Seq[T], Callable[[Iterable[T]], Seq[T]]]:
    """
    Returns a new Seq skipping the first elements as long as the predicate is true.

    :param predicate: A function that evaluates each element to a boolean.
    :param sequence: The sequence
    :return: A new Seq instance with the elements dropped as long as the predicate
    is true.
    """
    if sequence is None:
        return lambda s: Seq(s).drop_while(predicate)
    return Seq(sequence).drop_while(predicate)


@overload
def take(
    n: int,
    sequence: Iterable[T],
) -> Seq[T]:
    """
    Returns a new Seq consisting of the first n elements of the original sequence.

    :param n: The number of elements to take.
    :param sequence: The sequence
    :return: A new Seq instance with at most n elements.
    """


@overload
def take(n: int) -> Callable[[Iterable[T]], Seq[T]]:
    """
    Builds a function that returns a new Seq consisting of the first n elements of the
    original sequence.

    :param n: The number of elements to take.
    :return: Function that returns a new Seq consisting of the first n elements of the
    original sequence.
    """


def take(
    n: int,
    sequence: Optional[Iterable[T]] = None,
) -> Union[Seq[T], Callable[[Iterable[T]], Seq[T]]]:
    """
    Returns a new Seq consisting of the first n elements of the original sequence.

    :param n: The number of elements to take.
    :param sequence: The sequence. If None, a callable is returned.
    :return: A new Seq instance with at most n elements.
    """
    if sequence is None:
        return lambda s: Seq(s).take(n)
    return Seq(sequence).take(n)


@overload
def take_while(
    predicate: Callable[[T], bool],
    sequence: Iterable[T],
) -> Seq[T]:
    """
    Returns a new Seq consisting of the elements of the original sequence as long as
    the predicate is true.

    :param predicate: A function that evaluates each element to a boolean.
    :param sequence: The sequence
    :return: A new Seq instance with elements as long as the predicate is true.
    """


@overload
def take_while(
    predicate: Callable[[T], bool],
) -> Callable[[Iterable[T]], Seq[T]]:
    """
    Builds a function that returns a new Seq consisting of the elements of the original
    sequence as long as the predicate is true.

    :param predicate: A function that evaluates each element to a boolean.
    :return: Function that returns a new Seq consisting of the elements of the original
    sequence as long as the predicate is true.
    """


def take_while(
    predicate: Callable[[T], bool],
    sequence: Optional[Iterable[T]] = None,
) -> Union[Seq[T], Callable[[Iterable[T]], Seq[T]]]:
    """
    Returns a new Seq consisting of the elements of the original sequence as long as
    the predicate is true.

    :param predicate: A function that evaluates each element to a boolean.
    :param sequence: The sequence. If None, a callable is returned.
    :return: A new Seq instance with elements as long as the predicate is true.
    """
    if sequence is None:
        return lambda s: Seq(s).take_while(predicate)
    return Seq(sequence).take_while(predicate)


@overload
def sorted_by(
    key_func: Callable[[T], CT],
    sequence: Iterable[T],
) -> Seq[T]:
    """
    Returns a new Seq with elements sorted according to the specified key function.

    :param key_func: A function that extracts a comparison key from each element.
    :param sequence: The sequence
    :return: A new Seq instance with elements sorted by the key function.
    """


@overload
def sorted_by(key_func: Callable[[T], CT]) -> Callable[[Iterable[T]], Seq[T]]:
    """
    Builds a function that returns a new Seq with elements sorted according to the
    specified key function.

    :param key_func: A function that extracts a comparison key from each element.
    :return: Function that returns a new Seq with elements sorted according to the
    specified key function.
    """


def sorted_by(
    key_func: Callable[[T], CT],
    sequence: Optional[Iterable[T]] = None,
) -> Union[Seq[T], Callable[[Iterable[T]], Seq[T]]]:
    """
    Returns a new Seq with elements sorted according to the specified key function.

    :param key_func: A function that extracts a comparison key from each element.
    :param sequence: The sequence. If None, a callable is returned.
    :return: A new Seq instance with elements sorted by the key function.
    """
    if sequence is None:
        return lambda s: Seq(s).sorted_by(key_func)
    return Seq(sequence).sorted_by(key_func)


def sorted_desc(sequence: Iterable[CT]) -> Seq[CT]:
    """
    Returns a new Seq with elements sorted in descending order.

    :param sequence: The sequence
    :return: A new Seq instance with elements sorted in descending order.
    """
    return Seq(sequence).sorted_desc()


@overload
def sorted_by_desc(
    key_func: Callable[[T], CT],
    sequence: Iterable[T],
) -> Seq[T]:
    """
    Returns a new Seq with elements sorted in descending order according to the
    specified key function.

    :param key_func: A function that extracts a comparison key from each element.
    :param sequence: The sequence
    :return: A new Seq instance with elements sorted by the key function in
    descending order.
    """


@overload
def sorted_by_desc(key_func: Callable[[T], CT]) -> Callable[[Iterable[T]], Seq[T]]:
    """
    Builds a function that returns a new Seq with elements sorted in descending order
    according to the specified key function.

    :param key_func: A function that extracts a comparison key from each element.
    :return: Function that returns a new Seq with elements sorted in descending order
    according to the specified key function.
    """


def sorted_by_desc(
    key_func: Callable[[T], CT],
    sequence: Optional[Iterable[T]] = None,
) -> Union[Seq[T], Callable[[Iterable[T]], Seq[T]]]:
    """
    Returns a new Seq with elements sorted in descending order according to the
    specified key function.

    :param key_func: A function that extracts a comparison key from each element.
    :param sequence: The sequence. If None, a callable is returned.
    :return: A new Seq instance with elements sorted by the key function in
    descending order.
    """
    if sequence is None:
        return lambda s: Seq(s).sorted_by_desc(key_func)
    return Seq(sequence).sorted_by_desc(key_func)


@overload
def chunked(
    size: int,
    sequence: Iterable[T],
) -> Seq[list[T]]:
    """
    Splits the sequence into chunks of the specified size.

    :param size: The size of each chunk.
    :param sequence: The sequence
    :return: A new Seq instance where each element is a list representing a chunk of
    the original sequence.
    """


@overload
def chunked(size: int) -> Callable[[Iterable[T]], Seq[list[T]]]:
    """
    Builds a function that splits the sequence into chunks of the specified size.

    :param size: The size of each chunk.
    :return: Function that splits the sequence into chunks of the specified size.
    """


def chunked(
    size: int,
    sequence: Optional[Iterable[T]] = None,
) -> Union[Seq[list[T]], Callable[[Iterable[T]], Seq[list[T]]]]:
    """
    Splits the sequence into chunks of the specified size.

    :param size: The size of each chunk.
    :param sequence: The sequence. If None, a callable is returned.
    :return: A new Seq instance where each element is a list representing a chunk of
    the original sequence.
    """
    if sequence is None:
        return lambda s: Seq(s).chunked(size)
    return Seq(sequence).chunked(size)


def distinct(sequence: Iterable[T]) -> Seq[T]:
    """
    Returns a new Seq with distinct elements from the original sequence.

    :param sequence: The sequence
    :return: A new Seq instance with unique elements.
    """
    return Seq(sequence).distinct()


@overload
def distinct_by(
    key_selector: Callable[[T], R],
    sequence: Iterable[T],
) -> Seq[T]:
    """
    Returns a new Seq with elements that are distinct based on the key returned by
    the given keySelector function.

    :param key_selector: A function that returns a comparison key for each element.
    :param sequence: The sequence
    :return: A new Seq instance with distinct elements based on the key.
    """


@overload
def distinct_by(
    key_selector: Callable[[T], R],
) -> Callable[[Iterable[T]], Seq[T]]:
    """
    Builds a function that returns a new Seq with elements that are distinct based on
    the key returned by the given keySelector function.

    :param key_selector: A function that returns a comparison key for each element.
    :return: Function that returns a new Seq with elements that are distinct based on
    the key returned by the given keySelector function.
    """


def distinct_by(
    key_selector: Callable[[T], R],
    sequence: Optional[Iterable[T]] = None,
) -> Union[Seq[T], Callable[[Iterable[T]], Seq[T]]]:
    """
    Returns a new Seq with elements that are distinct based on the key returned by
    the given keySelector function.

    :param key_selector: A function that returns a comparison key for each element.
    :param sequence: The sequence. If None, a callable is returned.
    :return: A new Seq instance with distinct elements based on the key.
    """
    if sequence is None:
        return lambda s: Seq(s).distinct_by(key_selector)
    return Seq(sequence).distinct_by(key_selector)


@overload
def partition(
    predicate: Callable[[T], bool],
    sequence: Iterable[T],
) -> tuple[list[T], list[T]]:
    """
    Splits the sequence into two sequences based on a predicate.

    :param predicate: The function to test each element of the sequence.
    :param sequence: The sequence
    :return: A tuple of two Seq instances: the first containing elements for which
    the predicate is True, and the second containing elements for which the
    predicate is False.
    """


@overload
def partition(
    predicate: Callable[[T], bool],
) -> Callable[[Iterable[T]], tuple[list[T], list[T]]]:
    """
    Builds a function that splits the sequence into two sequences based on a predicate.

    :param predicate: The function to test each element of the sequence.
    :return: Function that splits the sequence into two sequences based on a predicate.
    """


def partition(
    predicate: Callable[[T], bool],
    sequence: Optional[Iterable[T]] = None,
) -> Union[tuple[list[T], list[T]], Callable[[Iterable[T]], tuple[list[T], list[T]]]]:
    """
    Splits the sequence into two sequences based on a predicate.

    :param predicate: The function to test each element of the sequence.
    :param sequence: The sequence. If None, a callable is returned.
    :return: A tuple of two Seq instances: the first containing elements for which
    the predicate is True, and the second containing elements for which the
    predicate is False.
    """
    if sequence is None:
        return lambda s: Seq(s).partition(predicate)
    return Seq(sequence).partition(predicate)
