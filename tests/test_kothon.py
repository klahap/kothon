import pytest

from kothon import Seq


def test_filter():
    seq = Seq([1, 2, 3, 4, 5])
    filtered = seq.filter(lambda x: x % 2 == 0).to_list()
    assert filtered == [2, 4]


def test_filter_not_none():
    seq = Seq([1, None, 2, None, 3])
    filtered = seq.filter_not_none().to_list()
    assert filtered == [1, 2, 3]


def test_map():
    seq = Seq([1, 2, 3])
    mapped = seq.map(lambda x: x * x).to_list()
    assert mapped == [1, 4, 9]


def test_map_not_none():
    seq = Seq([1, 2, 3, 4])
    mapped = seq.map_not_none(lambda x: x * 2 if x % 2 == 0 else None).to_list()
    assert mapped == [4, 8]


def test_flat_map():
    seq = Seq([1, 2, 3])
    flat_mapped = seq.flat_map(lambda x: [x, x * 10]).to_list()
    assert flat_mapped == [1, 10, 2, 20, 3, 30]


def test_flatten():
    seq = Seq([[1, 2], [3, 4], [5]])
    flattened = seq.flatten().to_list()
    assert flattened == [1, 2, 3, 4, 5]


def test_associate():
    seq = Seq(["a", "bb", "ccc"])
    associated = seq.associate(lambda x: (x, len(x)))
    assert associated == {"a": 1, "bb": 2, "ccc": 3}


def test_associate_by():
    seq = Seq(["apple", "banana", "cherry"])
    associated_by = seq.associate_by(lambda x: x[0])
    assert associated_by == {"a": "apple", "b": "banana", "c": "cherry"}


def test_associate_with():
    seq = Seq([1, 2, 3])
    associated_with = seq.associate_with(lambda x: x * x)
    assert associated_with == {1: 1, 2: 4, 3: 9}


def test_group_by():
    seq = Seq(["one", "two", "three"])
    grouped = seq.group_by(lambda x: len(x))
    assert grouped == {3: ["one", "two"], 5: ["three"]}


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


def test_none():
    seq = Seq([1, 2, 3])
    assert seq.none(lambda x: x > 3)
    assert not seq.none(lambda x: x < 3)
    assert Seq([False, False, False]).none()
    assert not Seq([True, False, True]).none()


def test_any():
    seq = Seq([1, 2, 3])
    assert seq.any(lambda x: x == 2)
    assert not seq.any(lambda x: x == 4)
    assert Seq([True, False, True]).any()
    assert not Seq([False, False, False]).any()


def test_max():
    seq = Seq([1, 3, 2])
    assert seq.max() == 3


def test_max_or_none():
    assert Seq([]).max_or_none() is None
    assert Seq([1, 2, 3]).max_or_none() == 3


def test_max_by():
    seq = Seq(["a", "abc", "ab"])
    assert seq.max_by(lambda x: len(x)) == "abc"


def test_max_by_or_none():
    assert Seq([]).max_by_or_none(lambda x: len(x)) is None
    assert Seq(["a", "abc", "ab"]).max_by_or_none(lambda x: len(x)) == "abc"


def test_min():
    seq = Seq([3, 1, 2])
    assert seq.min() == 1


def test_min_or_none():
    assert Seq([]).min_or_none() is None
    assert Seq([3, 1, 2]).min_or_none() == 1


def test_min_by():
    seq = Seq(["abc", "a", "ab"])
    assert seq.min_by(lambda x: len(x)) == "a"


def test_min_by_or_none():
    assert Seq([]).min_by_or_none(lambda x: len(x)) is None
    assert Seq(["abc", "a", "ab"]).min_by_or_none(lambda x: len(x)) == "a"


def test_single():
    seq = Seq([5])
    assert seq.single() == 5
    with pytest.raises(ValueError):
        Seq([1, 2]).single()
    with pytest.raises(ValueError):
        Seq([]).single()


def test_single_or_none():
    assert Seq([5]).single_or_none() == 5
    assert Seq([1, 2]).single_or_none() is None
    assert Seq([]).single_or_none() is None


def test_first():
    seq = Seq([1, 2, 3])
    assert seq.first() == 1
    with pytest.raises(ValueError):
        Seq([]).first()


def test_first_or_none():
    assert Seq([1, 2, 3]).first_or_none() == 1
    assert Seq([]).first_or_none() is None


def test_last():
    seq = Seq([1, 2, 3, 4, 5])
    assert seq.last() == 5
    with pytest.raises(ValueError):
        Seq([]).last()  # Test for empty sequence

    seq = Seq(range(6))
    assert seq.last() == 5
    with pytest.raises(ValueError):
        Seq(range(0)).last()  # Test for empty sequence


def test_last_or_none():
    assert Seq([1, 2, 3, 4, 5]).last_or_none() == 5
    assert Seq([]).last_or_none() is None  # Test for empty sequence

    assert Seq(range(6)).last_or_none() == 5
    assert Seq(range(0)).last_or_none() is None  # Test for empty sequence


def test_drop():
    seq = Seq([1, 2, 3, 4, 5])
    assert seq.drop(2).to_list() == [3, 4, 5]
    assert seq.drop(0).to_list() == [1, 2, 3, 4, 5]
    assert seq.drop(10).to_list() == []


def test_drop_while():
    seq = Seq([1, 2, 3, 4, 5, 1])
    assert seq.drop_while(lambda x: x < 3).to_list() == [3, 4, 5, 1]
    assert seq.drop_while(lambda x: x < 6).to_list() == []


def test_take():
    seq = Seq([1, 2, 3, 4, 5])
    assert seq.take(3).to_list() == [1, 2, 3]
    assert seq.take(0).to_list() == []
    assert seq.take(10).to_list() == [1, 2, 3, 4, 5]


def test_take_while():
    seq = Seq([1, 2, 3, 4, 5, 1])
    assert seq.take_while(lambda x: x < 4).to_list() == [1, 2, 3]
    assert seq.take_while(lambda x: x < 6).to_list() == [1, 2, 3, 4, 5, 1]


def test_sorted():
    seq = Seq([3, 1, 4, 1, 5, 9, 2, 6])
    assert seq.sorted().to_list() == [1, 1, 2, 3, 4, 5, 6, 9]


def test_sorted_by():
    seq = Seq(["banana", "apple", "cherry", "date"])
    assert seq.sorted_by(lambda x: x[0]).to_list() == [
        "apple",
        "banana",
        "cherry",
        "date",
    ]


def test_sorted_desc():
    seq = Seq([3, 1, 4, 1, 5, 9, 2, 6])
    assert seq.sorted_desc().to_list() == [9, 6, 5, 4, 3, 2, 1, 1]


def test_sorted_by_desc():
    seq = Seq(["banana", "apple", "cherry", "date"])
    assert seq.sorted_by_desc(lambda x: len(x)).to_list() == [
        "banana",
        "cherry",
        "apple",
        "date",
    ]


def test_chunked():
    seq = Seq([1, 2, 3, 4, 5])
    assert seq.chunked(2).to_list() == [[1, 2], [3, 4], [5]]


def test_enumerated():
    seq = Seq(["a", "b", "c"])
    assert seq.enumerate().to_list() == [(0, "a"), (1, "b"), (2, "c")]


def test_shuffled():
    seq = Seq([1, 2, 3, 4, 5])
    shuffled_seq = seq.shuffled().to_list()
    assert set(shuffled_seq) == {1, 2, 3, 4, 5}
    assert len(shuffled_seq) == 5


def test_reduce():
    seq = Seq([1, 2, 3, 4])
    assert seq.reduce(lambda x, y: x + y) == 10
    with pytest.raises(TypeError):
        Seq([]).reduce(lambda x, y: x + y)  # Test for empty sequence


def test_reduce_or_none():
    assert Seq([1, 2, 3, 4]).reduce_or_none(lambda x, y: x + y) == 10
    assert Seq([]).reduce_or_none(lambda x, y: x + y) is None  # Test for empty sequence


def test_sum():
    seq = Seq([1, 2, 3, 4])
    assert seq.sum() == 10


def test_distinct():
    seq = Seq([1, 2, 2, 3, 3, 3])
    assert seq.distinct().to_list() == [1, 2, 3]


def test_distinct_by():
    seq = Seq(["apple", "banana", "pear", "apricot"])
    assert seq.distinct_by(lambda x: x[0]).to_list() == ["apple", "banana", "pear"]


def test_for_each():
    seq = Seq([1, 2, 3])
    output = []
    seq.for_each(lambda x: output.append(x * 2))
    assert output == [2, 4, 6]


def test_filter_is_instance():
    seq = Seq([1, "two", 3, "four", 5])
    assert seq.filter_is_instance(str).to_list() == ["two", "four"]


def test_join_to_string():
    seq = Seq(["apple", "banana", "cherry"])
    joined_str = seq.join_to_string(
        separator=", ",
        prefix="[",
        suffix="]",
    )
    assert joined_str == "[apple, banana, cherry]"


def test_partition():
    seq = Seq([1, 2, 3, 4, 5])
    evens, odds = seq.partition(lambda x: x % 2 == 0)
    assert evens.to_list() == [2, 4]
    assert odds.to_list() == [1, 3, 5]
