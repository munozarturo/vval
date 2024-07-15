<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://www.munozarturo.com/assets/vval/logo-long-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="https://www.munozarturo.com/assets/vval/-logo-long-light.svg">
    <img alt="vval" src="https://www.munozarturo.com/assets/vval/-logo-long-light.svg" width="50%" height="40%">
  </picture>
</p>

<!-- omit from toc -->
# vval: value validation

The `vval` module provides functions for input validation in python.

<!-- omit from toc -->
## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Basic Type Validation](#basic-type-validation)
  - [Iterable Validation](#iterable-validation)
  - [Option Validation](#option-validation)
  - [Filter Validation](#filter-validation)
- [Functionality Examples](#functionality-examples)
- [Notes](#notes)
- [Testing](#testing)
- [Packaging](#packaging)

## Installation

```bash
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

## Testing

```bash
pip install pytest
python pytest -m
```

## Packaging

```bash
pip install --upgrade setuptools wheel twine
python setup.py sdist bdist_wheel
twine upload dist/*
```
