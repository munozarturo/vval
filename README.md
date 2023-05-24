# vval-py

The ``vval`` module provides functions for input validation in python.

Installation:

```shell
pip install vval
```

Usage:

```python
from typing import Callable, Union
from vval import validate, validate_iterable

def f(x: int | str) -> None:
    validate(x, (int, str))
    ...
    
def g(x: Union[int, float]) -> None:
    validate(x, Union[int, float])
    ...
    
def h(x: Union[list, tuple] | dict | set) -> None:
    validate(x, (Union[list, tuple], dict, set))
    ...

def i(x: list[int | str | dict]) -> None:
    validate_iterable(x, (int, str, dict))
    ...
    
def j(x: list[int | str | dict | Union[float, Callable]]) -> None:
    validate_iterable(x, (int, str, dict, Union[float, Callable]))
    ...
```

Note: The API is still experimental.
      Will not validate beyond a certain depth.
      Will not validate generic types (except Union).  

Currently provided functions:

* ``validate``: Validate that an element is of a specified type.
* ``validate_iterable``: Validate that all elements in an iterable are of a specified type.

Functionality:

```python
from typing import Callable, Union
from vval import validate, validate_iterable

y: list = [1, 2, 3]
validate(y, list) # True

x: list = [1, 2, 3]
validate(x, int)
```

```text
...
TypeError: Expected 'int' for `x`, got: 'list'.
```
