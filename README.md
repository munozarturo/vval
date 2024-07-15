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
- [Development and Publishing](#development-and-publishing)
  - [Testing](#testing)
  - [CI/CD](#cicd)
  - [Publishing a New Version](#publishing-a-new-version)
  - [Manual Publishing (if needed)](#manual-publishing-if-needed)

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

## Development and Publishing

### Testing

Run tests locally:

```bash
pip install .[dev]
pytest
```

### CI/CD

This project uses GitHub Actions for Continuous Integration and Continuous Deployment:

1. **Pull Request Checks**: Automatically run tests on all pull requests to the main branch.
2. **Automated Publishing**: Triggers package build and publication to PyPI when a new version tag is pushed.

### Publishing a New Version

1. Create a new branch for the version bump:

   ```bash
   git checkout -b bump-version-x.y.z
   ```

2. Update the version in `setup.py` following [Semantic Versioning](https://semver.org/).

3. Commit changes:

   ```bash
   git add setup.py
   git commit -m "pack: bump version to x.y.z"
   ```

4. Push the branch and create a pull request:

   ```bash
   git push origin bump-version-x.y.z
   ```

   Then create a pull request on GitHub from this branch to main.

5. After the pull request is approved and merged, checkout and pull the updated main branch:

   ```bash
   git checkout main
   git pull origin main
   ```

6. Create and push a new tag:

   ```bash
   git tag vx.y.z
   git push origin vx.y.z
   ```

   Replace `x.y.z` with the new version number.

7. The GitHub Action will automatically build and publish the new version to PyPI.

### Manual Publishing (if needed)

Prerequisites:

```bash
pip install --upgrade setuptools wheel twine build
```

Build and publish:

```bash
rm -rf dist build *.egg-info
python -m build
twine check dist/*
twine upload dist/*
```

For TestPyPI (optional):

```bash
twine upload --repository testpypi dist/*
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ wreqs
```

Note: Manual publishing should only be necessary if the automated process fails.
