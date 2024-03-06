# pylint: disable=missing-module-docstring,missing-function-docstring
# pylint: disable=unnecessary-lambda-assignment,missing-module-docstring

import functools
import operator
import random
import pytest

from kothon import (
    Seq,
    associate,
    associate_by,
    associate_with,
    group_by,
    all_by,
    none_by,
    any_by,
    max_or_none,
    max_by,
    max_by_or_none,
    min_or_none,
    min_by,
    min_by_or_none,
    single,
    single_or_none,
    first,
    first_or_none,
    last,
    last_or_none,
    reduce_or_none,
    sum_or_none,
    join_to_string,
    filter_not_none,
    filter_is_instance,
    map_not_none,
    flat_map,
    flatten,
    drop,
    drop_while,
    take,
    take_while,
    sorted_by,
    sorted_desc,
    sorted_by_desc,
    chunked,
    shuffled,
    distinct,
    distinct_by,
    partition,
)


def test_filter() -> None:
    seq = Seq([1, 2, 3, 4, 5])
    r1: list[int] = seq.filter(lambda x: x % 2 == 0).to_list()
    assert r1 == [2, 4]


def test_filter_not_none() -> None:
    seq = Seq([1, None, 2, None, 3])
    r1: list[int] = seq.filter_not_none().to_list()
    r2: list[int] = filter_not_none(seq).to_list()
    assert r1 == r2 == [1, 2, 3]


def test_map() -> None:
    seq = Seq([1, 2, 3])
    r1: list[int] = seq.map(lambda x: x * x).to_list()
    assert r1 == [1, 4, 9]


def test_map_not_none() -> None:
    seq = Seq([1, 2, 3, 4])
    fun = lambda x: x * 2 if x % 2 == 0 else None
    r1: list[int] = seq.map_not_none(lambda x: x * 2 if x % 2 == 0 else None).to_list()
    r2: list[int] = map_not_none(seq, fun).to_list()
    assert r1 == r2 == [4, 8]


def test_flat_map() -> None:
    seq = Seq([1, 2, 3])
    fun = lambda x: [x, x * 10]
    r1: list[int] = seq.flat_map(fun).to_list()
    r2: list[int] = flat_map(seq, fun).to_list()
    assert r1 == r2 == [1, 10, 2, 20, 3, 30]


def test_flatten() -> None:
    seq: Seq[list[int]] = Seq([[1, 2], [3, 4], [5]])
    r1: list[int] = seq.flatten().to_list()
    r2: list[int] = flatten(seq).to_list()
    assert r1 == r2 == [1, 2, 3, 4, 5]


def test_associate() -> None:
    seq = Seq(["a", "bb", "ccc"])
    fun = lambda x: (x, len(x))
    r1: dict[str, int] = seq.associate(fun)
    r2: dict[str, int] = associate(seq, fun)
    assert r1 == r2 == {"a": 1, "bb": 2, "ccc": 3}


def test_associate_by() -> None:
    seq = Seq(["apple", "banana", "cherry"])
    fun = lambda x: x[0]
    r1: dict[str, str] = seq.associate_by(fun)
    r2: dict[str, str] = associate_by(seq, fun)
    assert r1 == r2 == {"a": "apple", "b": "banana", "c": "cherry"}


def test_associate_with() -> None:
    seq = Seq([1, 2, 3])
    fun = lambda x: x * x
    r1: dict[int, int] = seq.associate_with(fun)
    r2: dict[int, int] = associate_with(seq, fun)
    assert r1 == r2 == {1: 1, 2: 4, 3: 9}


def test_group_by() -> None:
    seq = Seq(["one", "two", "three"])
    fun = len
    r1: dict[int, list[str]] = seq.group_by(fun)
    r2: dict[int, list[str]] = group_by(seq, fun)
    assert r1 == r2 == {3: ["one", "two"], 5: ["three"]}


def test_to_list() -> None:
    seq = Seq([1, 2, 3])
    r1: list[int] = seq.to_list()
    r2: list[int] = list(seq)
    assert r1 == r2 == [1, 2, 3]


def test_to_set() -> None:
    seq = Seq([1, 2, 2, 3, 3, 3])
    r1: set[int] = seq.to_set()
    r2: set[int] = set(seq)
    assert r1 == r2 == {1, 2, 3}


def test_to_frozenset() -> None:
    seq = Seq([1, 2, 2, 3, 3, 3])
    r1: frozenset[int] = seq.to_frozenset()
    r2: frozenset[int] = frozenset(seq)
    assert r1 == r2 == {1, 2, 3}


def test_all() -> None:
    seq = Seq([1, 2, 3])
    assert seq.all(lambda x: x < 4)
    assert not seq.all(lambda x: x < 3)
    assert Seq([True, True, True]).all()
    assert not Seq([True, False, True]).all()
    assert all_by(seq, lambda x: x < 4)
    assert not all_by(seq, lambda x: x < 3)


def test_none() -> None:
    seq = Seq([1, 2, 3])
    assert seq.none(lambda x: x > 3)
    assert not seq.none(lambda x: x < 3)
    assert Seq([False, False, False]).none()
    assert not Seq([True, False, True]).none()
    assert none_by(seq, lambda x: x > 3)
    assert not none_by(seq, lambda x: x < 3)


def test_any() -> None:
    seq = Seq([1, 2, 3])
    assert seq.any(lambda x: x == 2)
    assert not seq.any(lambda x: x == 4)
    assert Seq([True, False, True]).any()
    assert not Seq([False, False, False]).any()
    assert any_by(seq, lambda x: x == 2)
    assert not any_by(seq, lambda x: x == 4)


def test_max() -> None:
    seq = Seq([1, 3, 2])
    r1: int = seq.max()
    r2: int = max(seq)
    assert r1 == r2 == 3
    with pytest.raises(ValueError):
        Seq([]).max()


def test_max_or_none() -> None:
    seq = Seq([1, 2, 3])
    r1: int | None = seq.max_or_none()
    r2: int | None = max_or_none(seq)
    assert r1 == r2 == 3
    assert Seq([]).max_or_none() is None
    assert max_or_none([]) is None


def test_max_by() -> None:
    seq = Seq(["a", "abc", "ab"])
    fun = len
    r1: str = seq.max_by(fun)
    r2: str = max_by(seq, fun)
    assert r1 == r2 == "abc"
    with pytest.raises(ValueError):
        Seq([]).max_by(fun)
    with pytest.raises(ValueError):
        max_by([], fun)


def test_max_by_or_none() -> None:
    seq = Seq(["a", "bcd", "ef"])
    fun = len
    r1: str | None = seq.max_by_or_none(fun)
    r2: str | None = max_by_or_none(seq, fun)
    assert r1 == r2 == "bcd"

    seq = Seq([])
    assert seq.max_by_or_none(fun) is None
    assert max_by_or_none(seq, fun) is None

    seq = Seq(["abc"])
    r1 = seq.max_by_or_none(fun)
    r2 = max_by_or_none(seq, fun)
    assert r1 == r2 == "abc"


def test_min() -> None:
    seq = Seq([3, 1, 2])
    r1: int = seq.min()
    r2: int = min(seq)
    assert r1 == r2 == 1
    with pytest.raises(ValueError):
        Seq([]).min()


def test_min_or_none() -> None:
    seq = Seq([3, 1, 2])
    r1: int | None = seq.min_or_none()
    r2: int | None = min_or_none(seq)
    assert r1 == r2 == 1
    assert Seq([]).min_or_none() is None
    assert min_or_none([]) is None


def test_min_by() -> None:
    seq = Seq(["abc", "a", "ab"])
    fun = len
    r1: str = seq.min_by(fun)
    r2: str = min_by(seq, fun)
    assert r1 == r2 == "a"
    with pytest.raises(ValueError):
        Seq([]).min_by(fun)
    with pytest.raises(ValueError):
        min_by([], fun)


def test_min_by_or_none() -> None:
    seq = Seq(["a", "bcd", "ef"])
    fun = len
    r1: str | None = seq.min_by_or_none(fun)
    r2: str | None = min_by_or_none(seq, fun)
    assert r1 == r2 == "a"

    seq = Seq([])
    assert seq.min_by_or_none(fun) is None
    assert min_by_or_none(seq, fun) is None

    seq = Seq(["abc"])
    r1 = seq.min_by_or_none(fun)
    r2 = min_by_or_none(seq, fun)
    assert r1 == r2 == "abc"


def test_single() -> None:
    seq = Seq([5])
    r1: int = seq.single()
    r2: int = single(seq)
    assert r1 == r2 == 5
    with pytest.raises(ValueError):
        Seq([1, 2]).single()
    with pytest.raises(ValueError):
        Seq([]).single()
    with pytest.raises(ValueError):
        single([1, 2])
    with pytest.raises(ValueError):
        single([])


def test_single_or_none() -> None:
    seq = Seq([5])
    r1: int | None = seq.single_or_none()
    r2: int | None = single_or_none(seq)
    assert r1 == r2 == 5
    assert Seq([1, 2]).single_or_none() is None
    assert Seq([]).single_or_none() is None
    assert single_or_none([1, 2]) is None
    assert single_or_none([]) is None


def test_first() -> None:
    seq = Seq([5, 4, 3])
    r1: int = seq.first()
    r2: int = first(seq)
    assert r1 == r2 == 5
    with pytest.raises(ValueError):
        Seq([]).first()
    with pytest.raises(ValueError):
        first([])


def test_first_or_none() -> None:
    seq = Seq([5, 4, 3])
    r1: int | None = seq.first_or_none()
    r2: int | None = first_or_none(seq)
    assert r1 == r2 == 5
    assert Seq([]).first_or_none() is None
    assert first_or_none([]) is None


def test_last() -> None:
    seq = Seq([1, 2, 3, 4, 5])
    r1: int = seq.last()
    r2: int = last(seq)
    assert r1 == r2 == 5
    with pytest.raises(ValueError):
        Seq([]).last()  # Test for empty sequence
    with pytest.raises(ValueError):
        last([])  # Test for empty sequence

    seq = Seq(range(6))
    r1 = seq.last()
    r2 = last(seq)
    assert r1 == r2 == 5
    with pytest.raises(ValueError):
        Seq(range(0)).last()  # Test for empty sequence
    with pytest.raises(ValueError):
        last(range(0))  # Test for empty sequence


def test_last_or_none() -> None:
    seq = Seq([1, 2, 3, 4, 5])
    r1: int | None = seq.last_or_none()
    r2: int | None = last_or_none(seq)
    assert r1 == r2 == 5
    assert Seq([]).last_or_none() is None  # Test for empty sequence
    assert last_or_none([]) is None  # Test for empty sequence

    seq = Seq(range(6))
    r1 = seq.last_or_none()
    r2 = last_or_none(seq)
    assert r1 == r2 == 5
    assert Seq(range(0)).last_or_none() is None  # Test for empty sequence
    assert last_or_none(range(0)) is None  # Test for empty sequence


def test_drop() -> None:
    seq = Seq([1, 2, 3, 4, 5])

    n = 2
    r1: list[int] = seq.drop(n).to_list()
    r2: list[int] = drop(seq, n).to_list()
    assert r1 == r2 == [3, 4, 5]

    n = 0
    r1 = seq.drop(n).to_list()
    r2 = drop(seq, n).to_list()
    assert r1 == r2 == [1, 2, 3, 4, 5]

    n = 10
    r1 = seq.drop(n).to_list()
    r2 = drop(seq, n).to_list()
    assert not r1 and not r2


def test_drop_while() -> None:
    seq = Seq([1, 2, 3, 4, 5, 1])

    fun = lambda x: x < 3
    r1: list[int] = seq.drop_while(fun).to_list()
    r2: list[int] = drop_while(seq, fun).to_list()
    assert r1 == r2 == [3, 4, 5, 1]

    fun = lambda x: x < 6
    r1 = seq.drop_while(fun).to_list()
    r2 = drop_while(seq, fun).to_list()
    assert not r1 and not r2


def test_take() -> None:
    seq = Seq([1, 2, 3, 4, 5])

    n = 3
    r1: list[int] = seq.take(n).to_list()
    r2: list[int] = take(seq, n).to_list()
    assert r1 == r2 == [1, 2, 3]

    n = 0
    r1 = seq.take(n).to_list()
    r2 = take(seq, n).to_list()
    assert not r1 and not r2

    n = 10
    r1 = seq.take(n).to_list()
    r2 = take(seq, n).to_list()
    assert r1 == r2 == [1, 2, 3, 4, 5]


def test_take_while() -> None:
    seq = Seq([1, 2, 3, 4, 5, 1])

    fun = lambda x: x < 4
    r1: list[int] = seq.take_while(fun).to_list()
    r2: list[int] = take_while(seq, fun).to_list()
    assert r1 == r2 == [1, 2, 3]

    fun = lambda x: x < 1
    r1 = seq.take_while(fun).to_list()
    r2 = take_while(seq, fun).to_list()
    assert not r1 and not r2

    fun = lambda x: x < 6
    r1 = seq.take_while(fun).to_list()
    r2 = take_while(seq, fun).to_list()
    assert r1 == r2 == [1, 2, 3, 4, 5, 1]


def test_sorted() -> None:
    seq = Seq([3, 1, 4, 1, 5, 9, 2, 6])
    r1: list[int] = seq.sorted().to_list()
    r2: list[int] = sorted(seq)
    assert r1 == r2 == [1, 1, 2, 3, 4, 5, 6, 9]


def test_sorted_by() -> None:
    seq = Seq(["banana", "apple", "cherry", "date"])
    fun = lambda x: x[0]
    r1: list[str] = seq.sorted_by(fun).to_list()
    r2: list[str] = sorted_by(seq, fun).to_list()
    assert r1 == r2 == ["apple", "banana", "cherry", "date"]


def test_sorted_desc() -> None:
    seq = Seq([3, 1, 4, 1, 5, 9, 2, 6])
    r1: list[int] = seq.sorted_desc().to_list()
    r2: list[int] = sorted_desc(seq).to_list()
    assert r1 == r2 == [9, 6, 5, 4, 3, 2, 1, 1]


def test_sorted_by_desc() -> None:
    seq = Seq(["banana", "apple", "cherry", "date"])
    fun = len
    r1: list[str] = seq.sorted_by_desc(fun).to_list()
    r2: list[str] = sorted_by_desc(seq, fun).to_list()
    assert r1 == r2 == ["banana", "cherry", "apple", "date"]


def test_chunked() -> None:
    seq = Seq([1, 2, 3, 4, 5])
    n = 2
    r1: list[list[int]] = seq.chunked(n).to_list()
    r2: list[list[int]] = chunked(seq, n).to_list()
    assert r1 == r2 == [[1, 2], [3, 4], [5]]

    with pytest.raises(ValueError):
        seq.chunked(0)
    with pytest.raises(ValueError):
        chunked(seq, 0)


def test_enumerated() -> None:
    seq = Seq(["a", "b", "c"])
    r1: list[tuple[int, str]] = seq.enumerate().to_list()
    r2: list[tuple[int, str]] = list(enumerate(seq))
    assert r1 == r2 == [(0, "a"), (1, "b"), (2, "c")]


def test_shuffled() -> None:
    seq = Seq(range(128))
    r1: list[int] = seq.shuffled().to_list()
    assert r1 != list(range(128))
    assert set(r1) == set(range(128))
    assert len(r1) == 128

    r2: list[int] = shuffled(seq).to_list()
    assert r2 != list(range(128))
    assert set(r2) == set(range(128))
    assert len(r2) == 128

    assert r1 != r2

    seq = Seq([1, 2, 3, 4, 5])
    r1 = seq.shuffled(random.Random(42)).to_list()
    r2 = shuffled(seq, random.Random(42)).to_list()
    assert r1 == r2 == [4, 2, 3, 5, 1]


def test_reduce() -> None:
    seq = Seq([1, 2, 3, 4])
    fun = operator.add
    r1: int = seq.reduce(fun)
    r2: int = functools.reduce(fun, seq)
    assert r1 == r2 == 10
    with pytest.raises(TypeError):
        Seq([]).reduce(fun)


def test_reduce_or_none() -> None:
    seq = Seq([1, 2, 3, 4])
    fun = operator.add
    r1: int | None = seq.reduce_or_none(fun)
    r2: int | None = reduce_or_none(seq, fun)
    assert r1 == r2 == 10
    assert Seq([]).reduce_or_none(fun) is None
    assert reduce_or_none([], fun) is None


def test_sum() -> None:
    seq = Seq([1, 2, 3, 4])
    r1: int = seq.sum()
    r2: int = sum(seq)
    assert r1 == r2 == 10
    with pytest.raises(TypeError):
        Seq([]).sum()


def test_sum_or_none() -> None:
    seq = Seq([1, 2, 3, 4])
    r1: int | None = seq.sum_or_none()
    r2: int | None = sum_or_none(seq)
    assert r1 == r2 == 10
    assert Seq([]).sum_or_none() is None
    assert sum_or_none([]) is None


def test_distinct() -> None:
    seq = Seq([3, 2, 2, 1, 3, 3, 1, 3])
    r1: list[int] = seq.distinct().to_list()
    r2: list[int] = distinct(seq).to_list()
    assert r1, r2 == [3, 1, 2]


def test_distinct_by() -> None:
    seq = Seq(["apple", "banana", "pear", "apricot"])
    fun = lambda x: x[0]
    r1: list[str] = seq.distinct_by(fun).to_list()
    r2: list[str] = distinct_by(seq, fun).to_list()
    assert r1 == r2 == ["apple", "banana", "pear"]


def test_for_each() -> None:
    seq = Seq([1, 2, 3])
    output = []
    seq.for_each(lambda x: output.append(x * 2))
    assert output == [2, 4, 6]


def test_filter_is_instance() -> None:
    seq = Seq([1, "two", 3, "four", 5])
    r1: list[str] = seq.filter_is_instance(str).to_list()
    r2: list[str] = filter_is_instance(seq, str).to_list()
    assert r1 == r2 == ["two", "four"]


def test_join_to_string() -> None:
    seq = Seq(["apple", "banana", "cherry"])
    r1: str = seq.join_to_string(separator=", ", prefix="[", suffix="]")
    r2: str = join_to_string(seq, separator=", ", prefix="[", suffix="]")
    assert r1 == r2 == "[apple, banana, cherry]"


def test_partition() -> None:
    seq = Seq([1, 2, 3, 4, 5])
    fun = lambda x: x % 2 == 0
    r1: tuple[list[int], list[int]] = seq.partition(fun)
    r2: tuple[list[int], list[int]] = partition(seq, fun)
    assert r1 == r2 == ([2, 4], [1, 3, 5])
