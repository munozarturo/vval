# Value Validate (vval)

The `vval` module provides functions for input validation in python.

## Installation

```shell
pip install vval
```

## Usage

Import and use the `validate`, `validate_iterable`, `validate_option`, and `validate_filter` functions from the `vval` module.

### Basic Type Validation

```python
from typing import Union
from vval import validate

def f(x: int | str) -> None:
    validate(x, (int, str))
    ...

def g(x: Union[int, float]) -> None:
    validate(x, Union[int, float])
    ...

def h(x: Union[list, tuple] | dict | set) -> None:
    validate(x, (Union[list, tuple], dict, set))
    ...
```

### Iterable Validation

```python
from typing import Callable, Union
from vval import validate_iterable

def i(x: list[int | str | dict]) -> None:
    validate_iterable(x, (int, str, dict))
    ...

def j(x: list[int | str | dict | Union[float, Callable]]) -> None:
    validate_iterable(x, (int, str, dict, Union[float, Callable]))
    ...
```

### Option Validation

```python
from vval import validate_option

def k(x: str) -> None:
    validate_option(x, ["apple", "banana", "cherry"])
    ...
```

### Filter Validation

```python
from vval import validate_filter

def positive_filter(value):
    return value > 0

def l(x: int) -> None:
    validate_filter(x, positive_filter)
    ...
```

## Functionality Examples

```python
from vval import validate

y: list = [1, 2, 3]
validate(y, list) # True

x: list = [1, 2, 3]
validate(x, int) # Raises TypeError: Expected 'int' for `x`, got: 'list'.
```

## Notes

- The API is still experimental and subject to changes.
- Will not validate beyond a certain depth.
- Will not validate generic types (except Union).

Currently provided functions:

- `validate`: Validate that an element is of a specified type.
- `validate_iterable`: Validate that all elements in an iterable are of a specified type.
- `validate_option`: Validates that a value is among a set of options.
- `validate_filter`: Validates that a value passes a specified filter function.
