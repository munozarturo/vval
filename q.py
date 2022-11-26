from typing import Callable, Union
from vval import validate, validate_iterable

x: list = [1, 2, 3]
validate(x, int)