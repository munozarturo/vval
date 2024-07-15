<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://www.munozarturo.com/assets/vval/logo-github-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="https://www.munozarturo.com/assets/vval/logo-github-light.svg">
    <img alt="vval" src="https://www.munozarturo.com/assets/vval/logo-github-light.svg" width="50%" height="40%">
  </picture>
</div>

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
- [Packaging and Publishing](#packaging-and-publishing)
  - [Prerequisites](#prerequisites)
  - [Building the Package](#building-the-package)
  - [Checking the Distribution](#checking-the-distribution)
  - [Uploading to TestPyPI (Optional)](#uploading-to-testpypi-optional)
  - [Publishing to PyPI](#publishing-to-pypi)
  - [Versioning](#versioning)
  - [Git Tagging](#git-tagging)

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

## Packaging and Publishing

### Prerequisites

Ensure you have the latest versions of required tools:

```bash
pip install --upgrade setuptools wheel twine build
```

### Building the Package

1. Clean any existing builds:

    ```bash
    rm -rf dist build *.egg-info
    ```

2. Build the package:

    ```bash
    python -m build
    ```

This command creates both source (.tar.gz) and wheel (.whl) distributions in the `dist/` directory.

### Checking the Distribution

Before uploading, check if your package description will render correctly on PyPI:

```bash
twine check dist/*
```

### Uploading to TestPyPI (Optional)

It's a good practice to test your package on TestPyPI before publishing to the main PyPI:

```bash
twine upload --repository testpypi dist/*
```

You can then install your package from TestPyPI to verify it works correctly:

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ vval
```

### Publishing to PyPI

When you're ready to publish to the main PyPI:

```bash
twine upload dist/*
```

### Versioning

Remember to update the version number in `setup.py` before building and publishing a new release. Follow Semantic Versioning guidelines (<https://semver.org/>).

### Git Tagging

After a successful publish, tag your release in git:

git tag v0.1.x  # Replace with your version number
git push origin v0.1.x
