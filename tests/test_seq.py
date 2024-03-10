# pylint: disable=missing-module-docstring,missing-function-docstring

import functools
import operator
import random
from typing import cast, Callable, Optional, Iterable

import pytest

from kothon import (
    Seq,
    to_list,
    to_set,
    to_frozenset,
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
    kothon_filter,
    filter_not_none,
    filter_is_instance,
    map_not_none,
    kothon_map,
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
    distinct,
    distinct_by,
    partition,
)


def test_filter() -> None:
    seq = Seq([1, 2, 3, 4, 5])
    fun: Callable[[int], bool] = lambda x: x % 2 == 0
    r1: list[int] = seq.filter(fun).to_list()
    _1: list[str] = seq.filter(fun).to_list()  # type: ignore[assignment]
    r2: list[int] = kothon_filter(fun)(seq).to_list()
    _2: list[str] = kothon_filter(fun)(seq).to_list()  # type: ignore[assignment]
    assert r1 == r2 == [2, 4]


def test_filter_not_none() -> None:
    seq = Seq([1, None, 2, None, 3])
    r1: list[int] = seq.filter_not_none().to_list()
    _1: list[str] = seq.filter_not_none().to_list()  # type: ignore[assignment]
    r2: list[int] = filter_not_none(seq).to_list()
    _2: list[str] = filter_not_none(seq).to_list()  # type: ignore[assignment]
    assert r1 == r2 == [1, 2, 3]


def test_map() -> None:
    seq = Seq([1, 2, 3])
    fun: Callable[[int], int] = lambda x: x * x
    r1: list[int] = seq.map(fun).to_list()
    _1: list[str] = seq.map(fun).to_list()  # type: ignore[assignment]
    r2: list[int] = kothon_map(fun)(seq).to_list()
    _2: list[str] = kothon_map(fun)(seq).to_list()  # type: ignore[assignment]
    assert r1 == r2 == [1, 4, 9]


def test_map_not_none() -> None:
    seq = Seq([1, 2, 3, 4])
    fun: Callable[[int], Optional[int]] = lambda x: x * 2 if x % 2 == 0 else None
    r1: list[int] = seq.map_not_none(fun).to_list()
    _1: list[str] = seq.map_not_none(fun).to_list()  # type: ignore[assignment]
    r2: list[int] = map_not_none(fun, seq).to_list()
    _2: list[str] = map_not_none(fun, seq).to_list()  # type: ignore[assignment]
    r3: list[int] = map_not_none(fun)(seq).to_list()
    _3: list[str] = map_not_none(fun)(seq).to_list()  # type: ignore[assignment]
    assert r1 == r2 == r3 == [4, 8]


def test_flat_map() -> None:
    seq = Seq([1, 2, 3])
    fun: Callable[[int], list[int]] = lambda x: [x, x * 10]
    r1: list[int] = seq.flat_map(fun).to_list()
    _1: list[str] = seq.flat_map(fun).to_list()  # type: ignore[assignment]
    r2: list[int] = flat_map(fun, seq).to_list()
    _2: list[str] = flat_map(fun, seq).to_list()  # type: ignore[assignment]
    r3: list[int] = flat_map(fun)(seq).to_list()
    _3: list[str] = flat_map(fun)(seq).to_list()  # type: ignore[assignment]
    assert r1 == r2 == r3 == [1, 10, 2, 20, 3, 30]


def test_flatten() -> None:
    seq: Seq[Iterable[int]] = Seq([[1, 2], [3, 4], [5]])
    r1: list[int] = seq.flatten().to_list()
    _1: list[str] = seq.flatten().to_list()  # type: ignore[assignment]
    r2: list[int] = flatten(seq).to_list()
    _2: list[str] = flatten(seq).to_list()  # type: ignore[assignment]
    assert r1 == r2 == [1, 2, 3, 4, 5]


def test_associate() -> None:
    seq = Seq(["a", "bb", "ccc"])
    fun: Callable[[str], tuple[str, int]] = lambda x: (x, len(x))
    r1: dict[str, int] = seq.associate(fun)
    _1: dict[str, str] = seq.associate(fun)  # type: ignore[arg-type]
    r2: dict[str, int] = associate(fun, seq)
    _2: dict[str, str] = associate(fun, seq)  # type: ignore[arg-type]
    r3: dict[str, int] = associate(fun)(seq)
    _3: dict[str, str] = associate(fun)(seq)  # type: ignore[assignment]
    assert r1 == r2 == r3 == {"a": 1, "bb": 2, "ccc": 3}


def test_associate_by() -> None:
    seq = Seq(["apple", "banana", "cherry"])
    fun: Callable[[str], str] = lambda x: x[0]
    r1: dict[str, str] = seq.associate_by(fun)
    _1: dict[str, int] = seq.associate_by(fun)  # type: ignore[assignment]
    r2: dict[str, str] = associate_by(fun, seq)
    _2: dict[str, int] = associate_by(fun, seq)  # type: ignore[arg-type]
    r3: dict[str, str] = associate_by(fun)(seq)
    _3: dict[str, int] = associate_by(fun)(seq)  # type: ignore[assignment]
    assert r1 == r2 == r3 == {"a": "apple", "b": "banana", "c": "cherry"}


def test_associate_with() -> None:
    seq = Seq([1, 2, 3])
    fun: Callable[[int], int] = lambda x: x * x
    r1: dict[int, int] = seq.associate_with(fun)
    _1: dict[int, str] = seq.associate_with(fun)  # type: ignore[arg-type]
    r2: dict[int, int] = associate_with(fun, seq)
    _2: dict[int, str] = associate_with(fun, seq)  # type: ignore[arg-type]
    r3: dict[int, int] = associate_with(fun)(seq)
    _3: dict[int, str] = associate_with(fun)(seq)  # type: ignore[assignment]
    assert r1 == r2 == r3 == {1: 1, 2: 4, 3: 9}


def test_group_by() -> None:
    seq = Seq(["one", "two", "three"])
    fun: Callable[[str], int] = len
    r1: dict[int, list[str]] = seq.group_by(fun)
    _1: dict[int, list[int]] = seq.group_by(fun)  # type: ignore[assignment]
    r2: dict[int, list[str]] = group_by(fun, seq)
    _2: dict[int, list[int]] = group_by(fun, seq)  # type: ignore[arg-type]
    r3: dict[int, list[str]] = group_by(fun)(seq)
    _3: dict[int, list[int]] = group_by(fun)(seq)  # type: ignore[assignment]
    assert r1 == r2 == r3 == {3: ["one", "two"], 5: ["three"]}


def test_to_list() -> None:
    seq = Seq([1, 2, 3])
    r1: list[int] = seq.to_list()
    _1: list[str] = seq.to_list()  # type: ignore[assignment]
    r2: list[int] = list(seq)
    _2: list[str] = list(seq)  # type: ignore[arg-type]
    r3: list[int] = to_list(seq)
    _3: list[str] = to_list(seq)  # type: ignore[arg-type]
    assert r1 == r2 == r3 == [1, 2, 3]


def test_to_set() -> None:
    seq = Seq([1, 2, 2, 3, 3, 3])
    r1: set[int] = seq.to_set()
    _1: set[str] = seq.to_set()  # type: ignore[assignment]
    r2: set[int] = set(seq)
    _2: set[str] = set(seq)  # type: ignore[arg-type]
    r3: set[int] = to_set(seq)
    _3: set[str] = to_set(seq)  # type: ignore[arg-type]
    assert r1 == r2 == r3 == {1, 2, 3}


def test_to_frozenset() -> None:
    seq = Seq([1, 2, 2, 3, 3, 3])
    r1: frozenset[int] = seq.to_frozenset()
    _1: frozenset[str] = seq.to_frozenset()  # type: ignore[assignment]
    r2: frozenset[int] = frozenset(seq)
    _2: frozenset[str] = frozenset(seq)  # type: ignore[arg-type]
    r3: frozenset[int] = to_frozenset(seq)
    _3: frozenset[str] = to_frozenset(seq)  # type: ignore[arg-type]
    assert r1 == r2 == r3 == {1, 2, 3}


def test_all() -> None:
    seq = Seq([1, 2, 3])
    assert seq.all(lambda x: x < 4)
    assert not seq.all(lambda x: x < 3)
    assert Seq([True, True, True]).all()
    assert not Seq([True, False, True]).all()
    assert all_by(lambda x: x < 4, seq)
    assert not all_by(lambda x: x < 3, seq)
    assert all_by(cast(Callable[[int], bool], lambda x: x < 4))(seq)
    assert not all_by(cast(Callable[[int], bool], lambda x: x < 3))(seq)


def test_none() -> None:
    seq = Seq([1, 2, 3])
    assert seq.none(lambda x: x > 3)
    assert not seq.none(lambda x: x < 3)
    assert Seq([False, False, False]).none()
    assert not Seq([True, False, True]).none()
    assert none_by(lambda x: x > 3, seq)
    assert not none_by(lambda x: x < 3, seq)
    assert none_by(cast(Callable[[int], bool], lambda x: x > 3))(seq)
    assert not none_by(cast(Callable[[int], bool], lambda x: x < 3))(seq)


def test_any() -> None:
    seq = Seq([1, 2, 3])
    assert seq.any(lambda x: x == 2)
    assert not seq.any(lambda x: x == 4)
    assert Seq([True, False, True]).any()
    assert not Seq([False, False, False]).any()
    assert any_by(lambda x: x == 2, seq)
    assert not any_by(lambda x: x == 4, seq)
    assert any_by(lambda x: x == 2)(seq)
    assert not any_by(lambda x: x == 4)(seq)


def test_max() -> None:
    seq = Seq([1, 3, 2])
    r1: int = seq.max()
    _1: str = seq.max()  # type: ignore[assignment]
    r2: int = max(seq)
    _2: str = max(seq)  # type: ignore[assignment]
    assert r1 == r2 == 3
    with pytest.raises(ValueError):
        Seq([]).max()


def test_max_or_none() -> None:
    seq = Seq([1, 2, 3])
    r1: Optional[int] = seq.max_or_none()
    _1: int = seq.max_or_none()  # type: ignore[assignment]
    r2: Optional[int] = max_or_none(seq)
    _2: int = max_or_none(seq)  # type: ignore[assignment]
    assert r1 == r2 == 3
    assert Seq([]).max_or_none() is None
    assert max_or_none([]) is None


def test_max_by() -> None:
    seq = Seq(["a", "abc", "ab"])
    fun: Callable[[str], int] = len
    r1: str = seq.max_by(fun)
    _1: int = seq.max_by(fun)  # type: ignore[assignment]
    r2: str = max_by(fun, seq)
    _2: int = max_by(fun, seq)  # type: ignore[assignment]
    r3: str = max_by(fun)(seq)
    _3: int = max_by(fun)(seq)  # type: ignore[assignment]
    assert r1 == r2 == r3 == "abc"
    with pytest.raises(ValueError):
        Seq([]).max_by(fun)
    with pytest.raises(ValueError):
        max_by(fun, [])
    with pytest.raises(ValueError):
        max_by(fun)([])


def test_max_by_or_none() -> None:
    seq = Seq(["a", "bcd", "ef"])
    fun: Callable[[str], int] = len
    r1: Optional[str] = seq.max_by_or_none(fun)
    _1: str = seq.max_by_or_none(fun)  # type: ignore[assignment]
    r2: Optional[str] = max_by_or_none(fun, seq)
    _2: str = max_by_or_none(fun, seq)  # type: ignore[assignment]
    r3: Optional[str] = max_by_or_none(fun)(seq)
    _3: str = max_by_or_none(fun)(seq)  # type: ignore[assignment]
    assert r1 == r2 == r3 == "bcd"

    seq = Seq([])
    assert seq.max_by_or_none(fun) is None
    assert max_by_or_none(fun, seq) is None
    assert max_by_or_none(fun)(seq) is None

    seq = Seq(["abc"])
    r1 = seq.max_by_or_none(fun)
    r2 = max_by_or_none(fun, seq)
    r3 = max_by_or_none(fun)(seq)
    assert r1 == r2 == r3 == "abc"


def test_min() -> None:
    seq = Seq([3, 1, 2])
    r1: int = seq.min()
    _1: str = seq.min()  # type: ignore[assignment]
    r2: int = min(seq)
    _2: str = min(seq)  # type: ignore[assignment]
    assert r1 == r2 == 1
    with pytest.raises(ValueError):
        Seq([]).min()


def test_min_or_none() -> None:
    seq = Seq([3, 1, 2])
    r1: Optional[int] = seq.min_or_none()
    _1: int = seq.min_or_none()  # type: ignore[assignment]
    r2: Optional[int] = min_or_none(seq)
    _2: int = min_or_none(seq)  # type: ignore[assignment]
    assert r1 == r2 == 1
    assert Seq([]).min_or_none() is None
    assert min_or_none([]) is None


def test_min_by() -> None:
    seq = Seq(["abc", "a", "ab"])
    fun: Callable[[str], int] = len
    r1: str = seq.min_by(fun)
    _1: int = seq.min_by(fun)  # type: ignore[assignment]
    r2: str = min_by(fun, seq)
    _2: int = min_by(fun, seq)  # type: ignore[assignment]
    r3: str = min_by(fun)(seq)
    _3: int = min_by(fun)(seq)  # type: ignore[assignment]
    assert r1 == r2 == r3 == "a"
    with pytest.raises(ValueError):
        Seq([]).min_by(fun)
    with pytest.raises(ValueError):
        min_by(fun, [])
    with pytest.raises(ValueError):
        min_by(fun)([])


def test_min_by_or_none() -> None:
    seq = Seq(["a", "bcd", "ef"])
    fun: Callable[[str], int] = len
    r1: Optional[str] = seq.min_by_or_none(fun)
    _1: str = seq.min_by_or_none(fun)  # type: ignore[assignment]
    r2: Optional[str] = min_by_or_none(fun, seq)
    _2: str = min_by_or_none(fun, seq)  # type: ignore[assignment]
    r3: Optional[str] = min_by_or_none(fun)(seq)
    _3: str = min_by_or_none(fun)(seq)  # type: ignore[assignment]
    assert r1 == r2 == r3 == "a"

    seq = Seq([])
    assert seq.min_by_or_none(fun) is None
    assert min_by_or_none(fun, seq) is None
    assert min_by_or_none(fun)(seq) is None

    seq = Seq(["abc"])
    r1 = seq.min_by_or_none(fun)
    r2 = min_by_or_none(fun, seq)
    r3 = min_by_or_none(fun)(seq)
    assert r1 == r2 == r3 == "abc"


def test_single() -> None:
    seq = Seq([5])
    r1: int = seq.single()
    _1: str = seq.single()  # type: ignore[assignment]
    r2: int = single(seq)
    _2: str = single(seq)  # type: ignore[assignment]
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
    r1: Optional[int] = seq.single_or_none()
    _1: int = seq.single_or_none()  # type: ignore[assignment]
    r2: Optional[int] = single_or_none(seq)
    _2: int = single_or_none(seq)  # type: ignore[assignment]
    assert r1 == r2 == 5
    assert Seq([1, 2]).single_or_none() is None
    assert Seq([]).single_or_none() is None
    assert single_or_none([1, 2]) is None
    assert single_or_none([]) is None


def test_first() -> None:
    seq = Seq([5, 4, 3])
    r1: int = seq.first()
    _1: str = seq.first()  # type: ignore[assignment]
    r2: int = first(seq)
    _2: str = first(seq)  # type: ignore[assignment]
    assert r1 == r2 == 5
    with pytest.raises(ValueError):
        Seq([]).first()
    with pytest.raises(ValueError):
        first([])


def test_first_or_none() -> None:
    seq = Seq([5, 4, 3])
    r1: Optional[int] = seq.first_or_none()
    _1: int = seq.first_or_none()  # type: ignore[assignment]
    r2: Optional[int] = first_or_none(seq)
    _2: int = first_or_none(seq)  # type: ignore[assignment]
    assert r1 == r2 == 5
    assert Seq([]).first_or_none() is None
    assert first_or_none([]) is None


def test_last() -> None:
    seq = Seq([1, 2, 3, 4, 5])
    r1: int = seq.last()
    _1: str = seq.last()  # type: ignore[assignment]
    r2: int = last(seq)
    _2: str = last(seq)  # type: ignore[assignment]
    assert r1 == r2 == 5
    with pytest.raises(ValueError):
        Seq([]).last()
    with pytest.raises(ValueError):
        last([])

    seq = Seq(range(6))
    r1 = seq.last()
    r2 = last(seq)
    assert r1 == r2 == 5
    with pytest.raises(ValueError):
        Seq(range(0)).last()
    with pytest.raises(ValueError):
        last(range(0))


def test_last_or_none() -> None:
    seq = Seq([1, 2, 3, 4, 5])
    r1: Optional[int] = seq.last_or_none()
    _1: int = seq.last_or_none()  # type: ignore[assignment]
    r2: Optional[int] = last_or_none(seq)
    _2: int = last_or_none(seq)  # type: ignore[assignment]
    assert r1 == r2 == 5
    assert Seq([]).last_or_none() is None
    assert last_or_none([]) is None

    seq = Seq(range(6))
    r1 = seq.last_or_none()
    r2 = last_or_none(seq)
    assert r1 == r2 == 5
    assert Seq(range(0)).last_or_none() is None
    assert last_or_none(range(0)) is None


def test_drop() -> None:
    seq = Seq([1, 2, 3, 4, 5])

    n = 2
    r1: list[int] = seq.drop(n).to_list()
    _1: list[str] = seq.drop(n).to_list()  # type: ignore[assignment]
    r2: list[int] = drop(n, seq).to_list()
    _2: list[str] = drop(n, seq).to_list()  # type: ignore[assignment]
    r3: list[int] = drop(n)(seq).to_list()
    _3: list[str] = drop(n)(seq).to_list()  # type: ignore[assignment]
    assert r1 == r2 == r3 == [3, 4, 5]

    n = 0
    r1 = seq.drop(n).to_list()
    r2 = drop(n, seq).to_list()
    r3 = drop(n)(seq).to_list()
    assert r1 == r2 == r3 == [1, 2, 3, 4, 5]

    n = 10
    r1 = seq.drop(n).to_list()
    r2 = drop(n, seq).to_list()
    r3 = drop(n)(seq).to_list()
    assert not r1 and not r2 and not r3


def test_drop_while() -> None:
    seq = Seq([1, 2, 3, 4, 5, 1])

    fun1: Callable[[int], bool] = lambda x: x < 3
    r1: list[int] = seq.drop_while(fun1).to_list()
    _1: list[str] = seq.drop_while(fun1).to_list()  # type: ignore[assignment]
    r2: list[int] = drop_while(fun1, seq).to_list()
    _2: list[str] = drop_while(fun1, seq).to_list()  # type: ignore[assignment]
    r3: list[int] = drop_while(fun1)(seq).to_list()
    _3: list[str] = drop_while(fun1)(seq).to_list()  # type: ignore[assignment]
    assert r1 == r2 == r3 == [3, 4, 5, 1]

    fun2: Callable[[int], bool] = lambda x: x < 6
    r1 = seq.drop_while(fun2).to_list()
    r2 = drop_while(fun2, seq).to_list()
    r3 = drop_while(fun2)(seq).to_list()
    assert not r1 and not r2 and not r3


def test_take() -> None:
    seq = Seq([1, 2, 3, 4, 5])

    n = 3
    r1: list[int] = seq.take(n).to_list()
    _1: list[str] = seq.take(n).to_list()  # type: ignore[assignment]
    r2: list[int] = take(n, seq).to_list()
    _2: list[str] = take(n, seq).to_list()  # type: ignore[assignment]
    r3: list[int] = take(n)(seq).to_list()
    _3: list[str] = take(n)(seq).to_list()  # type: ignore[assignment]
    assert r1 == r2 == r3 == [1, 2, 3]

    n = 0
    r1 = seq.take(n).to_list()
    r2 = take(n, seq).to_list()
    r3 = take(n)(seq).to_list()
    assert not r1 and not r2 and not r3

    n = 10
    r1 = seq.take(n).to_list()
    r2 = take(n, seq).to_list()
    r3 = take(n)(seq).to_list()
    assert r1 == r2 == r3 == [1, 2, 3, 4, 5]


def test_take_while() -> None:
    seq = Seq([1, 2, 3, 4, 5, 1])

    fun1: Callable[[int], bool] = lambda x: x < 4
    r1: list[int] = seq.take_while(fun1).to_list()
    _1: list[str] = seq.take_while(fun1).to_list()  # type: ignore[assignment]
    r2: list[int] = take_while(fun1, seq).to_list()
    _2: list[str] = take_while(fun1, seq).to_list()  # type: ignore[assignment]
    r3: list[int] = take_while(fun1)(seq).to_list()
    _3: list[str] = take_while(fun1)(seq).to_list()  # type: ignore[assignment]
    assert r1 == r2 == r3 == [1, 2, 3]

    fun2: Callable[[int], bool] = lambda x: x < 1
    r1 = seq.take_while(fun2).to_list()
    r2 = take_while(fun2, seq).to_list()
    r3 = take_while(fun2)(seq).to_list()
    assert not r1 and not r2 and not r3

    fun3: Callable[[int], bool] = lambda x: x < 6
    r1 = seq.take_while(fun3).to_list()
    r2 = take_while(fun3, seq).to_list()
    r3 = take_while(fun3)(seq).to_list()
    assert r1 == r2 == r3 == [1, 2, 3, 4, 5, 1]


def test_sorted() -> None:
    seq = Seq([3, 1, 4, 1, 5, 9, 2, 6])
    r1: list[int] = seq.sorted().to_list()
    _1: list[str] = seq.sorted().to_list()  # type: ignore[assignment]
    r2: list[int] = sorted(seq)
    _2: list[str] = sorted(seq)  # type: ignore[arg-type]
    assert r1 == r2 == [1, 1, 2, 3, 4, 5, 6, 9]


def test_sorted_by() -> None:
    seq = Seq(["banana", "apple", "cherry", "damson"])
    fun: Callable[[str], int] = lambda x: ord(x[-1])
    r1: list[str] = seq.sorted_by(fun).to_list()
    _1: list[int] = seq.sorted_by(fun).to_list()  # type: ignore[assignment]
    r2: list[str] = sorted_by(fun, seq).to_list()
    _2: list[int] = sorted_by(fun, seq).to_list()  # type: ignore[assignment]
    r3: list[str] = sorted_by(fun)(seq).to_list()
    _3: list[int] = sorted_by(fun)(seq).to_list()  # type: ignore[assignment]
    assert r1 == r2 == r3 == ["banana", "apple", "damson", "cherry"]


def test_sorted_desc() -> None:
    seq = Seq([3, 1, 4, 1, 5, 9, 2, 6])
    r1: list[int] = seq.sorted_desc().to_list()
    _1: list[str] = seq.sorted_desc().to_list()  # type: ignore[assignment]
    r2: list[int] = sorted_desc(seq).to_list()
    _2: list[str] = sorted_desc(seq).to_list()  # type: ignore[assignment]
    assert r1 == r2 == [9, 6, 5, 4, 3, 2, 1, 1]


def test_sorted_by_desc() -> None:
    seq = Seq(["banana", "apple", "cherry", "damson"])
    fun: Callable[[str], int] = lambda x: ord(x[-1])
    r1: list[str] = seq.sorted_by_desc(fun).to_list()
    _1: list[int] = seq.sorted_by_desc(fun).to_list()  # type: ignore[assignment]
    r2: list[str] = sorted_by_desc(fun, seq).to_list()
    _2: list[int] = sorted_by_desc(fun, seq).to_list()  # type: ignore[assignment]
    r3: list[str] = sorted_by_desc(fun)(seq).to_list()
    _3: list[int] = sorted_by_desc(fun)(seq).to_list()  # type: ignore[assignment]
    assert r1 == r2 == r3 == ["cherry", "damson", "apple", "banana"]


def test_chunked() -> None:
    seq = Seq([1, 2, 3, 4, 5])
    n = 2
    r1: list[list[int]] = seq.chunked(n).to_list()
    _1: list[list[str]] = seq.chunked(n).to_list()  # type: ignore[assignment]
    r2: list[list[int]] = chunked(n, seq).to_list()
    _2: list[list[str]] = chunked(n, seq).to_list()  # type: ignore[assignment]
    r3: list[list[int]] = chunked(n)(seq).to_list()
    _3: list[list[str]] = chunked(n)(seq).to_list()  # type: ignore[assignment]
    assert r1 == r2 == r3 == [[1, 2], [3, 4], [5]]

    with pytest.raises(ValueError):
        seq.chunked(0)
    with pytest.raises(ValueError):
        chunked(0, seq)
    with pytest.raises(ValueError):
        chunked(0)(seq)


def test_enumerated() -> None:
    seq = Seq(["a", "b", "c"])
    r1: list[tuple[int, str]] = seq.enumerate().to_list()
    _1: list[tuple[int, int]] = seq.enumerate().to_list()  # type: ignore[assignment]
    r2: list[tuple[int, str]] = list(enumerate(seq))
    _2: list[tuple[int, int]] = list(enumerate(seq))  # type: ignore[arg-type]
    assert r1 == r2 == [(0, "a"), (1, "b"), (2, "c")]


def test_shuffled() -> None:
    seq = Seq(range(128))
    r1: list[int] = seq.shuffled().to_list()
    _1: list[str] = seq.shuffled().to_list()  # type: ignore[assignment]
    assert r1 != list(range(128))
    assert set(r1) == set(range(128))
    assert len(r1) == 128

    seq = Seq([1, 2, 3, 4, 5])
    r1 = seq.shuffled(random.Random(42)).to_list()
    assert r1 == [4, 2, 3, 5, 1]


def test_reduce() -> None:
    seq = Seq([1, 2, 3, 4])
    fun = operator.add
    r1: int = seq.reduce(fun)
    _1: str = seq.reduce(fun)  # type: ignore[assignment]
    r2: int = functools.reduce(fun, seq)
    _2: str = functools.reduce(fun, seq)  # type: ignore[assignment]
    assert r1 == r2 == 10
    with pytest.raises(TypeError):
        Seq([]).reduce(fun)


def test_reduce_or_none() -> None:
    seq = Seq([1, 2, 3, 4])
    fun = operator.add
    r1: Optional[int] = seq.reduce_or_none(fun)
    _1: int = seq.reduce_or_none(fun)  # type: ignore[assignment]
    r2: Optional[int] = reduce_or_none(fun, seq)
    _2: int = reduce_or_none(fun, seq)  # type: ignore[assignment]
    r3: Optional[int] = reduce_or_none(fun)(seq)
    _3: int = reduce_or_none(fun)(seq)  # type: ignore[assignment]
    assert r1 == r2 == r3 == 10
    assert Seq([]).reduce_or_none(fun) is None
    assert reduce_or_none(fun, []) is None
    assert reduce_or_none(fun)([]) is None


def test_sum() -> None:
    seq = Seq([1, 2, 3, 4])
    r1: int = seq.sum()
    _1: str = seq.sum()  # type: ignore[assignment]
    r2: int = sum(seq)
    _2: str = sum(seq)  # type: ignore[assignment]
    assert r1 == r2 == 10
    with pytest.raises(TypeError):
        Seq([]).sum()


def test_sum_or_none() -> None:
    seq = Seq([1, 2, 3, 4])
    r1: Optional[int] = seq.sum_or_none()
    _1: int = seq.sum_or_none()  # type: ignore[assignment]
    r2: Optional[int] = sum_or_none(seq)
    _2: int = sum_or_none(seq)  # type: ignore[assignment]
    assert r1 == r2 == 10
    assert Seq([]).sum_or_none() is None
    assert sum_or_none([]) is None


def test_distinct() -> None:
    seq = Seq([3, 2, 2, 1, 3, 3, 1, 3])
    r1: list[int] = seq.distinct().to_list()
    _1: list[str] = seq.distinct().to_list()  # type: ignore[assignment]
    r2: list[int] = distinct(seq).to_list()
    _2: list[str] = distinct(seq).to_list()  # type: ignore[assignment]
    assert r1, r2 == [3, 1, 2]


def test_distinct_by() -> None:
    seq = Seq(["apple", "banana", "pear", "apricot"])
    fun: Callable[[str], int] = lambda x: ord(x[0])
    r1: list[str] = seq.distinct_by(fun).to_list()
    _1: list[int] = seq.distinct_by(fun).to_list()  # type: ignore[assignment]
    r2: list[str] = distinct_by(fun, seq).to_list()
    _2: list[int] = distinct_by(fun, seq).to_list()  # type: ignore[assignment]
    r3: list[str] = distinct_by(fun)(seq).to_list()
    _3: list[int] = distinct_by(fun)(seq).to_list()  # type: ignore[assignment]
    assert r1 == r2 == r3 == ["apple", "banana", "pear"]


def test_for_each() -> None:
    seq = Seq([1, 2, 3])
    output = []
    seq.for_each(lambda x: output.append(x * 2))
    assert output == [2, 4, 6]


def test_filter_is_instance() -> None:
    seq = Seq([1, "two", 3, "four", 5])
    r1: list[str] = seq.filter_is_instance(str).to_list()
    _1: list[int] = seq.filter_is_instance(str).to_list()  # type: ignore[assignment]
    r2: list[str] = filter_is_instance(str, seq).to_list()
    _2: list[int] = filter_is_instance(str, seq).to_list()  # type: ignore[assignment]
    r3: list[str] = filter_is_instance(str)(seq).to_list()
    _3: list[int] = filter_is_instance(str)(seq).to_list()  # type: ignore[assignment]
    assert r1 == r2 == r3 == ["two", "four"]


def test_join_to_string() -> None:
    seq = Seq(["apple", "banana", "cherry"])
    r1: str = seq.join_to_string(separator=", ", prefix="[", suffix="]")
    _1: int = seq.join_to_string(  # type: ignore[assignment]
        separator=", ",
        prefix="[",
        suffix="]",
    )
    r2: str = join_to_string(separator=", ", prefix="[", suffix="]")(seq)
    _2: int = join_to_string(  # type: ignore[assignment]
        separator=", ",
        prefix="[",
        suffix="]",
    )(seq)
    assert r1 == r2 == "[apple, banana, cherry]"


def test_partition() -> None:
    seq = Seq([1, 2, 3, 4, 5])
    fun: Callable[[int], bool] = lambda x: x % 2 == 0
    r1: tuple[list[int], list[int]] = seq.partition(fun)
    _1: tuple[list[str], list[int]] = seq.partition(fun)  # type: ignore[assignment]
    r2: tuple[list[int], list[int]] = partition(fun, seq)
    _2: tuple[list[str], list[int]] = partition(fun, seq)  # type: ignore[assignment]
    r3: tuple[list[int], list[int]] = partition(fun)(seq)
    _3: tuple[list[str], list[int]] = partition(fun)(seq)  # type: ignore[assignment]
    assert r1 == r2 == r3 == ([2, 4], [1, 3, 5])
