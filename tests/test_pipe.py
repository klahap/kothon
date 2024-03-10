# pylint: disable=missing-module-docstring,missing-function-docstring

from functools import partial
from operator import add, mul
from typing import Callable

import pytest
from kothon import pipe, to_list, filter_not_none, kothon_filter, kothon_map

add_one: Callable[[int], int] = partial(add, 1)
double: Callable[[int], int] = partial(mul, 2)


@pytest.mark.parametrize("num_funcs", range(12))
def test_pipe(num_funcs: int) -> None:
    r1: int = pipe(0, *([add_one] * num_funcs))
    _1: str = pipe(0, *([add_one] * num_funcs))  # type: ignore[assignment]
    assert r1 == num_funcs


def test_pipe_with_args() -> None:
    r1: int = pipe(0, add_one, add_one, add_one)
    _1: str = pipe(0, add_one, add_one, add_one)  # type: ignore[assignment]
    assert r1 == 3


def test_numeric_pipe_to_str() -> None:
    filter_4: Callable[[int], bool] = lambda x: x % 4 == 0
    r1: list[str] = pipe(
        [0, 1, None, 2, 3, None, 4],
        filter_not_none,
        kothon_map(add_one),
        kothon_map(double),
        kothon_filter(filter_4),
        kothon_map(str),
    ).to_list()
    _1: list[int] = pipe(  # type: ignore[assignment]
        [0, 1, None, 2, 3, None, 4],
        filter_not_none,
        kothon_map(add_one),
        kothon_map(double),
        kothon_filter(filter_4),
        kothon_map(str),
    ).to_list()
    assert r1 == ["4", "8"]


def test_typing() -> None:
    r1: int = pipe(1, add_one)
    _1: str = pipe(1, add_one)  # type: ignore[assignment]
    assert r1 == 2

    r2: list[int] = pipe(range(10), to_list)
    _2: list[str] = pipe(range(10), to_list)  # type: ignore[arg-type]
    assert r2 == list(range(10))

    r3: list[str] = pipe(range(10), kothon_map(str), to_list)
    _3: list[int] = pipe(  # type: ignore[misc]
        range(10),
        kothon_map(str),
        to_list,
    )
    assert r3 == [str(i) for i in range(10)]
