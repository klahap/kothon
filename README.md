# Kothon

![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fklahap%2Fkothon%2Fmain%2Fpyproject.toml)
![GitHub License](https://img.shields.io/github/license/klahap/kothon)
![PyPI - Status](https://img.shields.io/pypi/status/kothon)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/klahap/kothon/tests.yml)
![Static Badge](https://img.shields.io/badge/coverage-100%25-success)

[//]: # (Using a static badge for 100% code coverage is justified because your test pipeline ensures coverage never falls below 100%, making dynamic updates unnecessary.)

Kothon is a Python library designed to bring the elegance and functionality of Kotlin's Sequence class into the Python
ecosystem. With an emphasis on functional programming paradigms, Kothon enables Python developers to leverage
lazy-evaluated sequences, allowing for efficient and expressive data processing pipelines.

## Features

- **Functional Programming**: Embrace functional programming with a rich set of operators
  like `map`, `filter`, `reduce`, and much more, enabling you to write more declarative and concise code.
- **Strongly Typed**: Leveraging Python's type hints for clearer, more robust code.
- **Lazy Evaluation**: Kothon sequences are evaluated lazily, meaning computations are deferred until the value is
  needed, enhancing performance especially for large datasets.
- **Interoperability**: Seamlessly integrate with existing Python codebases, enjoying the benefits of Kotlin-like
  sequences without disrupting your current workflow.
- **Easy to Use**: Kothon's API is designed to be intuitive for both Python and Kotlin developers, ensuring a smooth
  learning curve.

## Installation

To install Kothon, simply run the following command in your terminal:

```bash
pip install kothon
```

## Quick Start

Here's a quick example to get you started with Kothon:

```python
from kothon import Seq

input_data = [0, 1, None, 2, 3, None, 4]

# Apply some functional operations
result = Seq(input_data) \
    .filter_not_none() \
    .filter(lambda x: x % 2 == 0) \
    .map(lambda x: x * 2) \
    .to_list()

print(result)  # Output: [0, 4, 8]
```

Alternatively, utilize `pipe` for a more Pythonic approach.

```python
from kothon import pipe, filter_not_none, kothon_filter, kothon_map

input_data = [0, 1, None, 2, 3, None, 4]

# Apply some functional operations
result = pipe(
    input_data,
    filter_not_none,
    kothon_filter(lambda x: x % 2 == 0),
    kothon_map(lambda x: x * 2),
).to_list()

print(result)  # Output: [0, 4, 8]
```

## Existing functions in `Seq`

- [filter](#filter)
- [filter_not_none](#filter_not_none)
- [filter_is_instance](#filter_is_instance)
- [map](#map)
- [map_not_none](#map_not_none)
- [flat_map](#flat_map)
- [flatten](#flatten)
- [associate](#associate)
- [associate_by](#associate_by)
- [associate_with](#associate_with)
- [group_by](#group_by)
- [to_list](#to_list)
- [to_set](#to_set)
- [all](#all)
- [none](#none)
- [any](#any)
- [max](#max)
- [max_or_none](#max_or_none)
- [max_by](#max_by)
- [max_by_or_none](#max_by_or_none)
- [min](#min)
- [min_or_none](#min_or_none)
- [min_by](#min_by)
- [min_by_or_none](#min_by_or_none)
- [single](#single)
- [single_or_none](#single_or_none)
- [first](#first)
- [first_or_none](#first_or_none)
- [last](#last)
- [last_or_none](#last_or_none)
- [drop](#drop)
- [drop_while](#drop_while)
- [take](#take)
- [take_while](#take_while)
- [sorted](#sorted)
- [sorted_by](#sorted_by)
- [sorted_desc](#sorted_desc)
- [sorted_by_desc](#sorted_by_desc)
- [chunked](#chunked)
- [enumerate](#enumerate)
- [shuffled](#shuffled)
- [reduce](#reduce)
- [reduce_or_none](#reduce_or_none)
- [sum](#sum)
- [sum_or_none](#sum_or_none)
- [distinct](#distinct)
- [distinct_by](#distinct_by)
- [for_each](#for_each)
- [join_to_string](#join_to_string)
- [partition](#partition)

### filter

Filters elements based on a predicate.

```python
>>> from kothon import Seq
>>>
>>> seq = Seq([1, 2, 3, 4, 5])
>>> seq.filter(lambda x: x % 2 == 0).to_list()
[2, 4]
>>>
```

### filter_not_none

Filters out `None` values from the sequence.

```python
>>> from kothon import Seq
>>>
>>> seq = Seq([1, None, 2, None, 3])
>>> seq.filter_not_none().to_list()
[1, 2, 3]
>>>
```

### filter_is_instance

Filters elements of the sequence based on their type.

```python
>>> from kothon import Seq
>>>
>>> seq = Seq([1, 'two', 3, 'four', 5])
>>> seq.filter_is_instance(str).to_list()
['two', 'four']
>>>
```

### map

Applies a function to each element in the sequence.

```python
>>> from kothon import Seq
>>>
>>> seq = Seq([1, 2, 3])
>>> seq.map(lambda x: x * x).to_list()
[1, 4, 9]
>>>
```

### map_not_none

Applies a function to each element and filters out `None` results.

```python
>>> from kothon import Seq
>>>
>>> seq = Seq([1, 2, 3, 4])
>>> seq.map_not_none(lambda x: x * 2 if x % 2 == 0 else None).to_list()
[4, 8]
>>>
```

### flat_map

Applies a function to each element that returns an iterable and flattens the result.

```python
>>> from kothon import Seq
>>>
>>> seq = Seq([1, 2, 3])
>>> seq.flat_map(lambda x: [x, -x]).to_list()
[1, -1, 2, -2, 3, -3]
>>>
```

### flatten

Flattens a sequence of iterables into a single sequence.

```python
>>> from kothon import Seq
>>>
>>> seq = Seq([[1, 2], [3, 4], [5]])
>>> seq.flatten().to_list()
[1, 2, 3, 4, 5]
>>>
```

### associate

Transforms elements into key-value pairs and aggregates them into a dictionary.

```python
>>> from kothon import Seq
>>>
>>> seq = Seq(["a", "bb", "ccc"])
>>> seq.associate(lambda x: (x, len(x)))
{'a': 1, 'bb': 2, 'ccc': 3}
>>>
```

### associate_by

Creates a dictionary from the sequence by determining keys using a specified key selector function.

```python
>>> from kothon import Seq
>>>
>>> seq = Seq(["apple", "banana", "cherry"])
>>> seq.associate_by(lambda x: x[0])
{'a': 'apple', 'b': 'banana', 'c': 'cherry'}
>>>
```

### associate_with

Creates a dictionary from the sequence with elements as keys and values determined by a value selector function.

```python
>>> from kothon import Seq
>>>
>>> seq = Seq([1, 2, 3])
>>> seq.associate_with(lambda x: x * x)
{1: 1, 2: 4, 3: 9}
>>>
```

### group_by

Groups elements based on a key function.

```python
>>> from kothon import Seq
>>>
>>> seq = Seq(["one", "two", "three"])
>>> seq.group_by(len)
{3: ['one', 'two'], 5: ['three']}
>>>
```

### to_list

Converts the sequence to a list.

```python
>>> from kothon import Seq
>>>
>>> seq = Seq([1, 2, 3])
>>> seq.to_list()
[1, 2, 3]
>>>
```

### to_set

Converts the sequence to a set.

```python
>>> from kothon import Seq
>>>
>>> seq = Seq([1, 2, 2, 3, 3])
>>> seq.to_set()
{1, 2, 3}
>>>
```

### all

Checks if all elements satisfy a condition.

```python
>>> from kothon import Seq
>>>
>>> seq = Seq([2, 4, 6])
>>> seq.all(lambda x: x % 2 == 0)
True
>>> seq.all(lambda x: x > 5)
False
>>>
```

### none

Checks if no elements satisfy a condition.

```python
>>> from kothon import Seq
>>>
>>> seq = Seq([1, 3, 5])
>>> seq.none(lambda x: x % 2 == 0)
True
>>> seq.none(lambda x: x < 5)
False
>>>
```

### any

Checks if any elements satisfy a condition.

```python
>>> from kothon import Seq
>>>
>>> seq = Seq([1, 2, 3])
>>> seq.any(lambda x: x % 2 == 0)
True
>>> seq.any(lambda x: x > 5)
False
>>>
```

### max

Finds the maximum element.

```python
>>> from kothon import Seq
>>>
>>> seq = Seq([1, 3, 2])
>>> seq.max()
3
>>>
```

### max_or_none

Finds the maximum element, or returns `None` for an empty sequence.

```python
>>> from kothon import Seq
>>>
>>> seq = Seq([1, 3, 2])
>>> seq.max_or_none()
3
>>> seq = Seq([])
>>> seq.max_or_none()
>>>
```

### max_by

Finds the element which maximizes a specified function.

```python
>>> from kothon import Seq
>>>
>>> seq = Seq(['a', 'abc', 'ab'])
>>> seq.max_by(len)
'abc'
>>>
```

### max_by_or_none

Like `max_by`, but returns `None` for an empty sequence.

```python
>>> from kothon import Seq
>>>
>>> seq = Seq(['a', 'abc', 'ab'])
>>> seq.max_by_or_none(len)
'abc'
>>> seq = Seq([])
>>> seq.max_by_or_none(len)
>>>
```

### min

Finds the minimum element.

```python
>>> from kothon import Seq
>>>
>>> seq = Seq([3, 1, 2])
>>> seq.min()
1
>>>
```

### min_or_none

Finds the minimum element, or returns `None` for an empty sequence.

```python
>>> from kothon import Seq
>>>
>>> seq = Seq([1, 3, 2])
>>> seq.min_or_none()
1
>>> seq = Seq([])
>>> seq.min_or_none()
>>>
```

### min_by

Finds the element which minimizes a specified function.

```python
>>> from kothon import Seq
>>>
>>> seq = Seq(['abc', 'a', 'ab'])
>>> seq.min_by(len)
'a'
>>>
```

### min_by_or_none

Like `min_by`, but returns `None` for an empty sequence.

```python
>>> from kothon import Seq
>>>
>>> seq = Seq(['abc', 'a', 'ab'])
>>> seq.min_by_or_none(len)
'a'
>>> seq = Seq([])
>>> seq.min_by_or_none(len)
>>>
```

### single

Returns the single element of the sequence, and throws an error if the sequence does not contain exactly one element.

```python
>>> from kothon import Seq
>>>
>>> Seq([9]).single()
9
>>> # Seq([]).single()  # ERROR
>>> # Seq([1, 2]).single()  # ERROR
>>>
```

### single_or_none

Returns the single element of the sequence, or `None` if the sequence is empty. Throws an error if the sequence contains more than one element.

```python
>>> from kothon import Seq
>>>
>>> Seq([9]).single_or_none()
9
>>> Seq([]).single_or_none()
>>> Seq([1, 2]).single_or_none()
>>>
```

### first

Returns the first element of the sequence. Throws an error if the sequence is empty.

```python
>>> from kothon import Seq
>>>
>>> Seq([7, 8, 9]).first()
7
>>> # Seq([]).first()  # ERROR
>>>
```

### first_or_none

Returns the first element of the sequence, or `None` if the sequence is empty.

```python
>>> from kothon import Seq
>>>
>>> Seq([7, 8, 9]).first_or_none()
7
>>> Seq([]).first_or_none()
>>>
```

### last

Returns the last element of the sequence. Throws an error if the sequence is empty.

```python
>>> from kothon import Seq
>>>
>>> Seq([7, 8, 9]).last()
9
>>> # Seq([]).last()  # ERROR
>>>
```

### last_or_none

Returns the last element of the sequence, or `None` if the sequence is empty.

```python
>>> from kothon import Seq
>>>
>>> Seq([7, 8, 9]).last_or_none()
9
>>> Seq([]).last_or_none()
>>>
```

### drop

Returns a new sequence with the first `n` elements removed.

```python
>>> from kothon import Seq
>>>
>>> Seq([1, 2, 3, 4]).drop(2).to_list()
[3, 4]
>>>
```

### drop_while

Returns a new sequence by dropping elements as long as the predicate is true.

```python
>>> from kothon import Seq
>>>
>>> seq = Seq([1, 2, 3, 4, 1])
>>> seq.drop_while(lambda x: x < 3).to_list()
[3, 4, 1]
>>>
```

### take

Returns a new sequence containing the first `n` elements.

```python
>>> from kothon import Seq
>>>
>>> Seq([1, 2, 3, 4]).take(2).to_list()
[1, 2]
>>>
```

### take_while

Returns a new sequence by taking elements as long as the predicate is true.

```python
>>> from kothon import Seq
>>>
>>> seq = Seq([1, 2, 3, 4, 1])
>>> seq.take_while(lambda x: x < 3).to_list()
[1, 2]
>>>
```

### sorted

Returns a new sequence with elements sorted in ascending order.

```python
>>> from kothon import Seq
>>>
>>> Seq([3, 1, 4]).sorted().to_list()
[1, 3, 4]
>>>
```

### sorted_by

Sorts elements by a specified key function.

```python
>>> from kothon import Seq
>>>
>>> seq = Seq(['apple', 'banana', 'cherry'])
>>> seq.sorted_by(lambda x: x[0]).to_list()
['apple', 'banana', 'cherry']
>>>
```

### sorted_desc

Returns a new sequence with elements sorted in descending order.

```python
>>> from kothon import Seq
>>>
>>> Seq([3, 1, 4]).sorted_desc().to_list()
[4, 3, 1]
>>>
```

### sorted_by_desc

Sorts elements by a specified key function in descending order.

```python
>>> from kothon import Seq
>>>
>>> seq = Seq(['apple', 'banana', 'cherry'])
>>> seq.sorted_by_desc(lambda x: x[0]).to_list()
['cherry', 'banana', 'apple']
>>>
```

### chunked

Splits the sequence into chunks of the specified size.

```python
>>> from kothon import Seq
>>>
>>> Seq([1, 2, 3, 4, 5]).chunked(2).to_list()
[[1, 2], [3, 4], [5]]
>>>
```

### enumerate

Adds an index to each element of the sequence.

```python
>>> from kothon import Seq
>>>
>>> Seq(['a', 'b', 'c']).enumerate().to_list()
[(0, 'a'), (1, 'b'), (2, 'c')]
>>>
```

### shuffled

Returns a new sequence with elements shuffled in random order.

```python
>>> import random
>>> from kothon import Seq
>>>
>>> seq = Seq([1, 2, 3, 4, 5])
>>> rng = random.Random(42)  # custom pseudo-random number generator, Optional
>>> seq.shuffled(rng).to_list()
[4, 2, 3, 5, 1]
>>>
```

### reduce

Reduces the sequence to a single value by applying a binary operation. Throws an error if the sequence is empty.

```python
>>> from kothon import Seq
>>>
>>> Seq([1, 2, 3, 4]).reduce(lambda x, y: x + y)
10
>>>
```

### reduce_or_none

Like `reduce`, but returns `None` for an empty sequence.

```python
>>> from kothon import Seq
>>>
>>> Seq([1, 2, 3, 4]).reduce_or_none(lambda x, y: x + y)
10
>>> Seq([]).reduce_or_none(lambda x, y: x + y)
>>>
```

### sum

Sums the elements in the sequence. Throws an error if the sequence is empty.

```python
>>> from kothon import Seq
>>>
>>> Seq([1, 2, 3, 4]).sum()
10
>>>
```


### sum_or_none

Calculates the sum of all elements in the sequence, or returns `None` if the sequence is empty.

```python
>>> from kothon import Seq
>>>
>>> Seq([1, 2, 3, 4]).sum_or_none()
10
>>> Seq([]).sum_or_none()
>>>
```

### distinct

Returns a new sequence with distinct elements.

```python
>>> from kothon import Seq
>>>
>>> Seq([1, 2, 2, 3, 3]).distinct().to_list()
[1, 2, 3]
>>>
```

### distinct_by

Returns a new sequence with elements that are distinct based on the specified key function.

```python
>>> from kothon import Seq
>>>
>>> seq = Seq(['apple', 'banana', 'apricot'])
>>> seq.distinct_by(lambda x: x[0]).to_list()
['apple', 'banana']
>>>
```

### for_each

Applies an action to each element of the sequence.

```python
>>> from kothon import Seq
>>>
>>> result = []
>>> Seq([1, 2, 3]).for_each(lambda x: print(x))
1
2
3
>>>
```

### join_to_string

Concatenates elements of the sequence into a single string with specified separators and optional prefix/suffix.

```python
>>> from kothon import Seq
>>>
>>> seq = Seq(['apple', 'banana', 'cherry'])
>>> seq.join_to_string(separator=", ", prefix="[", suffix="]")
'[apple, banana, cherry]'
>>>
```

### partition

Splits the sequence into two sequences based on a predicate. The first sequence contains elements for which the predicate is true, and the second contains elements for which it is false.

```python
>>> from kothon import Seq
>>>
>>> seq = Seq([1, 2, 3, 4, 5])
>>> true_part, false_part = seq.partition(lambda x: x % 2 == 0)
>>> true_part
[2, 4]
>>> false_part
[1, 3, 5]
>>>
```

## Contributing

We welcome contributions! If you have improvements or bug fixes, please feel free to create a pull request.

## Acknowledgments

Kothon is inspired by the Kotlin Sequence class and the broader functional programming paradigm. We are grateful to the
Kotlin community for their innovative work, which has inspired the creation of this library.
