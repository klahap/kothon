"""
This module extends Python's functional programming capabilities, mainly through the
`pipe` function which facilitates function chaining for clear and maintainable code.
The `pipe` function enables the output of one function to be passed as the input to the
next, supporting a variety of use cases with its overloaded definitions. The code is
largely inspired by the `functools-extra` project available at
https://github.com/dennisrall/functools-extra
"""

# pylint: disable=too-many-arguments

from __future__ import annotations

from functools import reduce
from typing import Any, Callable, TypeVar, overload, Union

# pylint: disable=invalid-name
T0 = TypeVar("T0")
T1 = TypeVar("T1")
T2 = TypeVar("T2")
T3 = TypeVar("T3")
T4 = TypeVar("T4")
T5 = TypeVar("T5")
T6 = TypeVar("T6")
T7 = TypeVar("T7")
T8 = TypeVar("T8")
# pylint: enable=invalid-name


@overload
def pipe(value: T0) -> T0:
    """pipe"""


@overload
def pipe(value: T0, func1: Callable[[T0], T1]) -> T1:
    """pipe"""


@overload
def pipe(value: T0, func1: Callable[[T0], T1], func2: Callable[[T1], T2]) -> T2:
    """pipe"""


@overload
def pipe(
    value: T0,
    func1: Callable[[T0], T1],
    func2: Callable[[T1], T2],
    func3: Callable[[T2], T3],
) -> T3:
    """pipe"""


@overload
def pipe(
    value: T0,
    func1: Callable[[T0], T1],
    func2: Callable[[T1], T2],
    func3: Callable[[T2], T3],
    func4: Callable[[T3], T4],
) -> T4:
    """pipe"""


@overload
def pipe(
    value: T0,
    func1: Callable[[T0], T1],
    func2: Callable[[T1], T2],
    func3: Callable[[T2], T3],
    func4: Callable[[T3], T4],
    func5: Callable[[T4], T5],
) -> T5:
    """pipe"""


@overload
def pipe(
    value: T0,
    func1: Callable[[T0], T1],
    func2: Callable[[T1], T2],
    func3: Callable[[T2], T3],
    func4: Callable[[T3], T4],
    func5: Callable[[T4], T5],
    func6: Callable[[T5], T6],
) -> T6:
    """pipe"""


@overload
def pipe(
    value: T0,
    func1: Callable[[T0], T1],
    func2: Callable[[T1], T2],
    func3: Callable[[T2], T3],
    func4: Callable[[T3], T4],
    func5: Callable[[T4], T5],
    func6: Callable[[T5], T6],
    func7: Callable[[T6], T7],
) -> T7:
    """pipe"""


@overload
def pipe(
    value: T0,
    func1: Callable[[T0], T1],
    func2: Callable[[T1], T2],
    func3: Callable[[T2], T3],
    func4: Callable[[T3], T4],
    func5: Callable[[T4], T5],
    func6: Callable[[T5], T6],
    func7: Callable[[T6], T7],
    func8: Callable[[T7], T8],
    *funcs: Callable[[T8], T8],
) -> T8:
    """pipe"""


@overload
def pipe(
    value: T0,
    func1: Callable[[T0], T1],
    func2: Callable[[T1], T2],
    func3: Callable[[T2], T3],
    func4: Callable[[T3], T4],
    func5: Callable[[T4], T5],
    func6: Callable[[T5], T6],
    func7: Callable[[T6], T7],
    func8: Callable[[T7], T8],
    *funcs: Callable[[Any], Any],
) -> Any:
    """pipe"""


def pipe(  # type: ignore[misc]
    value: T0,
    *funcs: Callable[[Any], Any],
) -> Union[T0, T1, T2, T3, T4, T5, T6, T7, T8, Any]:
    """
    Processes a value through a sequence of functions, passing the result of each
    function as the input to the next.

    :param value: The initial value to process.
    :param funcs: Functions to apply to the value, in order.
    :return: The result of the last function in the chain, with the type depending on
    the sequence of functions applied.
    """
    return reduce(
        lambda v, func: func(v),
        funcs,
        value,
    )
