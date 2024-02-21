import random
import pytest

import kothon
from kothon import Seq


def test_filter():
    seq = Seq([1, 2, 3, 4, 5])
    filtered = seq.filter(lambda x: x % 2 == 0).to_list()
    assert filtered == [2, 4]


def test_filter_not_none():
    seq = Seq([1, None, 2, None, 3])
    filtered = seq.filter_not_none().to_list()
    assert filtered == [1, 2, 3]
    assert filtered == kothon.filter_not_none([1, None, 2, None, 3]).to_list()


def test_map():
    seq = Seq([1, 2, 3])
    mapped = seq.map(lambda x: x * x).to_list()
    assert mapped == [1, 4, 9]


def test_map_not_none():
    seq = Seq([1, 2, 3, 4])
    fun = lambda x: x * 2 if x % 2 == 0 else None
    mapped = seq.map_not_none(lambda x: x * 2 if x % 2 == 0 else None).to_list()
    assert mapped == [4, 8]
    assert mapped == kothon.map_not_none(seq, fun).to_list()


def test_flat_map():
    seq = Seq([1, 2, 3])
    fun = lambda x: [x, x * 10]
    flat_mapped = seq.flat_map(fun).to_list()
    assert flat_mapped == [1, 10, 2, 20, 3, 30]
    assert flat_mapped == kothon.flat_map(seq, fun).to_list()


def test_flatten():
    seq = Seq([[1, 2], [3, 4], [5]])
    flattened = seq.flatten().to_list()
    assert flattened == [1, 2, 3, 4, 5]
    assert flattened == kothon.flatten(seq).to_list()


def test_associate():
    seq = Seq(["a", "bb", "ccc"])
    fun = lambda x: (x, len(x))
    associated = seq.associate(fun)
    assert associated == {"a": 1, "bb": 2, "ccc": 3}
    assert associated == kothon.associate(seq, fun)


def test_associate_by():
    seq = Seq(["apple", "banana", "cherry"])
    fun = lambda x: x[0]
    associated_by = seq.associate_by(fun)
    assert associated_by == {"a": "apple", "b": "banana", "c": "cherry"}
    assert associated_by == kothon.associate_by(seq, fun)


def test_associate_with():
    seq = Seq([1, 2, 3])
    fun = lambda x: x * x
    associated_with = seq.associate_with(fun)
    assert associated_with == {1: 1, 2: 4, 3: 9}
    assert associated_with == kothon.associate_with(seq, fun)


def test_group_by():
    seq = Seq(["one", "two", "three"])
    fun = lambda x: len(x)
    grouped = seq.group_by(lambda x: len(x))
    assert grouped == {3: ["one", "two"], 5: ["three"]}
    assert grouped == kothon.group_by(seq, fun)


def test_to_list():
    seq = Seq([1, 2, 3])
    lst = seq.to_list()
    assert lst == [1, 2, 3]


def test_to_set():
    seq = Seq([1, 2, 2, 3, 3, 3])
    st = seq.to_set()
    assert st == {1, 2, 3}


def test_all():
    seq = Seq([1, 2, 3])
    assert seq.all(lambda x: x < 4)
    assert not seq.all(lambda x: x < 3)
    assert Seq([True, True, True]).all()
    assert not Seq([True, False, True]).all()
    assert kothon.all_by(seq, lambda x: x < 4)
    assert not kothon.all_by(seq, lambda x: x < 3)


def test_none():
    seq = Seq([1, 2, 3])
    assert seq.none(lambda x: x > 3)
    assert not seq.none(lambda x: x < 3)
    assert Seq([False, False, False]).none()
    assert not Seq([True, False, True]).none()
    assert kothon.none_by(seq, lambda x: x > 3)
    assert not kothon.none_by(seq, lambda x: x < 3)


def test_any():
    seq = Seq([1, 2, 3])
    assert seq.any(lambda x: x == 2)
    assert not seq.any(lambda x: x == 4)
    assert Seq([True, False, True]).any()
    assert not Seq([False, False, False]).any()
    assert kothon.any_by(seq, lambda x: x == 2)
    assert not kothon.any_by(seq, lambda x: x == 4)


def test_max():
    seq = Seq([1, 3, 2])
    assert seq.max() == 3
    with pytest.raises(ValueError):
        Seq([]).max()


def test_max_or_none():
    seq = Seq([1, 2, 3])
    assert Seq([]).max_or_none() is None
    assert seq.max_or_none() == kothon.max_or_none(seq) == 3
    assert kothon.max_or_none([]) is None


def test_max_by():
    seq = Seq(["a", "abc", "ab"])
    fun = lambda x: len(x)
    max_by = seq.max_by(fun)
    assert max_by == "abc"
    assert max_by == kothon.max_by(seq, fun)
    with pytest.raises(ValueError):
        Seq([]).max_by(fun)
    with pytest.raises(ValueError):
        kothon.max_by([], fun)


def test_max_by_or_none():
    seq = Seq(["a", "abc", "ab"])
    fun = lambda x: len(x)
    assert Seq([]).max_by_or_none(fun) is None
    assert seq.max_by_or_none(fun) == "abc"
    assert seq.max_by_or_none(fun) == kothon.max_by_or_none(seq, fun)


def test_min():
    seq = Seq([3, 1, 2])
    assert seq.min() == 1
    with pytest.raises(ValueError):
        Seq([]).min()


def test_min_or_none():
    seq = Seq([3, 1, 2])
    assert Seq([]).min_or_none() is None
    assert seq.min_or_none() == kothon.min_or_none(seq) == 1
    assert kothon.min_or_none([]) is None


def test_min_by():
    seq = Seq(["abc", "a", "ab"])
    fun = lambda x: len(x)
    assert seq.min_by(fun) == kothon.min_by(seq, fun) == "a"
    with pytest.raises(ValueError):
        Seq([]).min_by(fun)
    with pytest.raises(ValueError):
        kothon.min_by([], fun)


def test_min_by_or_none():
    seq = Seq(["abc", "a", "ab"])
    fun = lambda x: len(x)
    assert Seq([]).min_by_or_none(fun) is None
    assert seq.min_by_or_none(fun) == kothon.min_by_or_none(seq, fun) == "a"
    assert kothon.min_by_or_none([], fun) is None


def test_single():
    seq = Seq([5])
    assert seq.single() == kothon.single(seq) == 5
    with pytest.raises(ValueError):
        Seq([1, 2]).single()
    with pytest.raises(ValueError):
        Seq([]).single()
    with pytest.raises(ValueError):
        kothon.single([1, 2])
    with pytest.raises(ValueError):
        kothon.single([]).single()


def test_single_or_none():
    assert Seq([5]).single_or_none() == 5
    assert Seq([1, 2]).single_or_none() is None
    assert Seq([]).single_or_none() is None
    assert kothon.single_or_none([5]) == 5
    assert kothon.single_or_none([1, 2]) is None
    assert kothon.single_or_none([]) is None


def test_first():
    seq = Seq([1, 2, 3])
    assert seq.first() == kothon.first(seq) == 1
    with pytest.raises(ValueError):
        Seq([]).first()
    with pytest.raises(ValueError):
        kothon.first([])


def test_first_or_none():
    seq = Seq([1, 2, 3])
    assert seq.first_or_none() == kothon.first_or_none(seq) == 1
    assert Seq([]).first_or_none() is None
    assert kothon.first_or_none([]) is None


def test_last():
    seq = Seq([1, 2, 3, 4, 5])
    assert seq.last() == kothon.last(seq) == 5
    with pytest.raises(ValueError):
        Seq([]).last()  # Test for empty sequence
    with pytest.raises(ValueError):
        kothon.last([])  # Test for empty sequence

    seq = Seq(range(6))
    assert seq.last() == kothon.last(seq) == 5
    with pytest.raises(ValueError):
        Seq(range(0)).last()  # Test for empty sequence
    with pytest.raises(ValueError):
        kothon.last(range(0))  # Test for empty sequence


def test_last_or_none():
    seq = Seq([1, 2, 3, 4, 5])
    assert seq.last_or_none() == kothon.last_or_none(seq) == 5
    assert Seq([]).last_or_none() is None  # Test for empty sequence
    assert kothon.last_or_none([]) is None  # Test for empty sequence

    seq = Seq(range(6))
    assert seq.last_or_none() == kothon.last_or_none(seq) == 5
    assert Seq(range(0)).last_or_none() is None  # Test for empty sequence
    assert kothon.last_or_none(range(0)) is None  # Test for empty sequence


def test_drop():
    seq = Seq([1, 2, 3, 4, 5])
    assert seq.drop(2).to_list() == kothon.drop(seq, 2).to_list() == [3, 4, 5]
    assert seq.drop(0).to_list() == kothon.drop(seq, 0).to_list() == [1, 2, 3, 4, 5]
    assert seq.drop(10).to_list() == kothon.drop(seq, 10).to_list() == []


def test_drop_while():
    seq = Seq([1, 2, 3, 4, 5, 1])
    assert seq.drop_while(lambda x: x < 3).to_list() == [3, 4, 5, 1]
    assert seq.drop_while(lambda x: x < 6).to_list() == []
    assert kothon.drop_while(seq, lambda x: x < 3).to_list() == [3, 4, 5, 1]
    assert kothon.drop_while(seq, lambda x: x < 6).to_list() == []


def test_take():
    seq = Seq([1, 2, 3, 4, 5])
    assert seq.take(3).to_list() == kothon.take(seq, 3).to_list() == [1, 2, 3]
    assert seq.take(0).to_list() == kothon.take(seq, 0).to_list() == []
    assert seq.take(10).to_list() == kothon.take(seq, 10).to_list() == [1, 2, 3, 4, 5]


def test_take_while():
    seq = Seq([1, 2, 3, 4, 5, 1])
    assert seq.take_while(lambda x: x < 4).to_list() == [1, 2, 3]
    assert seq.take_while(lambda x: x < 6).to_list() == [1, 2, 3, 4, 5, 1]
    assert kothon.take_while(seq, lambda x: x < 4).to_list() == [1, 2, 3]
    assert kothon.take_while(seq, lambda x: x < 6).to_list() == [1, 2, 3, 4, 5, 1]


def test_sorted():
    seq = Seq([3, 1, 4, 1, 5, 9, 2, 6])
    assert seq.sorted().to_list() == [1, 1, 2, 3, 4, 5, 6, 9]


def test_sorted_by():
    seq = Seq(["banana", "apple", "cherry", "date"])
    fun = lambda x: x[0]
    sorted_by = seq.sorted_by(lambda x: x[0]).to_list()
    assert sorted_by == [
        "apple",
        "banana",
        "cherry",
        "date",
    ]
    assert sorted_by == kothon.sorted_by(seq, fun).to_list()


def test_sorted_desc():
    seq = Seq([3, 1, 4, 1, 5, 9, 2, 6])
    assert seq.sorted_desc().to_list() == [9, 6, 5, 4, 3, 2, 1, 1]
    assert seq.sorted_desc().to_list() == kothon.sorted_desc(seq).to_list()


def test_sorted_by_desc():
    seq = Seq(["banana", "apple", "cherry", "date"])
    fun = lambda x: len(x)
    sorted_by_desc = seq.sorted_by_desc(fun).to_list()
    assert sorted_by_desc == [
        "banana",
        "cherry",
        "apple",
        "date",
    ]
    assert sorted_by_desc == kothon.sorted_by_desc(seq, fun).to_list()


def test_chunked():
    seq = Seq([1, 2, 3, 4, 5])
    assert seq.chunked(2).to_list() == [[1, 2], [3, 4], [5]]
    assert seq.chunked(2).to_list() == kothon.chunked(seq, 2).to_list()


def test_enumerated():
    seq = Seq(["a", "b", "c"])
    assert seq.enumerate().to_list() == [(0, "a"), (1, "b"), (2, "c")]


def test_shuffled():
    seq = Seq(range(128))
    shuffled_seq = seq.shuffled().to_list()
    assert shuffled_seq != list(range(128))
    assert set(shuffled_seq) == set(range(128))
    assert len(shuffled_seq) == 128

    shuffled_seq = kothon.shuffled(seq).to_list()
    assert shuffled_seq != list(range(128))
    assert set(shuffled_seq) == set(range(128))
    assert len(shuffled_seq) == 128

    seq = Seq([1, 2, 3, 4, 5])
    shuffled_seq = seq.shuffled(random.Random(42)).to_list()
    assert shuffled_seq == [4, 2, 3, 5, 1]
    assert shuffled_seq == kothon.shuffled(seq, random.Random(42)).to_list()


def test_reduce():
    seq = Seq([1, 2, 3, 4])
    fun = lambda x, y: x + y
    assert seq.reduce(fun) == kothon.reduce(seq, fun) == 10
    with pytest.raises(TypeError):
        Seq([]).reduce(fun)
    with pytest.raises(TypeError):
        kothon.reduce([], fun)


def test_reduce_or_none():
    seq = Seq([1, 2, 3, 4])
    fun = lambda x, y: x + y
    assert seq.reduce_or_none(fun) == kothon.reduce_or_none(seq, fun) == 10
    assert Seq([]).reduce_or_none(fun) is None
    assert kothon.reduce_or_none([], fun) is None


def test_sum():
    seq = Seq([1, 2, 3, 4])
    assert seq.sum() == 10
    with pytest.raises(TypeError):
        Seq([]).sum()


def test_sum_or_none():
    seq = Seq([1, 2, 3, 4])
    assert seq.sum_or_none() == kothon.sum_or_none(seq) == 10
    assert Seq([]).sum_or_none() is None
    assert kothon.sum_or_none([]) is None


def test_distinct():
    seq = Seq([1, 2, 2, 3, 3, 3])
    assert seq.distinct().to_list() == kothon.distinct(seq).to_list() == [1, 2, 3]


def test_distinct_by():
    seq = Seq(["apple", "banana", "pear", "apricot"])
    fun = lambda x: x[0]
    assert seq.distinct_by(fun).to_list() == ["apple", "banana", "pear"]
    assert seq.distinct_by(fun).to_list() == kothon.distinct_by(seq, fun).to_list()


def test_for_each():
    seq = Seq([1, 2, 3])
    output = []
    seq.for_each(lambda x: output.append(x * 2))
    assert output == [2, 4, 6]


def test_filter_is_instance():
    seq = Seq([1, "two", 3, "four", 5])
    result = seq.filter_is_instance(str).to_list()
    assert result == kothon.filter_is_instance(seq, str).to_list() == ["two", "four"]


def test_join_to_string():
    seq = Seq(["apple", "banana", "cherry"])
    joined_str = seq.join_to_string(
        separator=", ",
        prefix="[",
        suffix="]",
    )
    assert joined_str == "[apple, banana, cherry]"
    assert joined_str == kothon.join_to_string(
        seq,
        separator=", ",
        prefix="[",
        suffix="]",
    )


def test_partition():
    seq = Seq([1, 2, 3, 4, 5])
    fun = lambda x: x % 2 == 0
    evens1, odds1 = seq.partition(fun)
    evens2, odds2 = kothon.partition(seq, fun)
    assert evens1.to_list() == evens2.to_list() == [2, 4]
    assert odds1.to_list() == odds2.to_list() == [1, 3, 5]
