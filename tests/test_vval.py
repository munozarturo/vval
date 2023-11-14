from typing import Union, List, Optional, Dict, Union
from vval.vval import is_union, is_iterable, is_generic, is_callable


def test_is_union():
    assert is_union(Union[int, str]) == True
    assert is_union(Optional[int]) == True  # Optional[int] is a Union[int, NoneType]
    assert is_union(int) == False
    assert is_union(List[int]) == False
    assert is_union(None) == False


def test_is_iterable():
    assert is_iterable([1, 2, 3])  # Lists are iterable
    assert is_iterable("hello")  # Strings are iterable
    assert is_iterable((1, 2, 3))  # Tuples are iterable
    assert not is_iterable(42)  # Integers are not iterable
    assert not is_iterable(None)  # None is not iterable

    class CustomIterable:
        def __iter__(self):
            return iter([1, 2, 3])

    assert is_iterable(CustomIterable())  # Custom iterables

    class NonIterable:
        pass

    assert not is_iterable(NonIterable())  # Non-iterable class instances


def test_is_generic():
    assert is_generic(List[int])  # Generic type
    assert is_generic(Dict[str, int])  # Generic type
    assert is_generic(Union[int, str])  # Union, a kind of generic
    assert not is_generic(int)  # Not a generic type
    assert not is_generic(3.14)  # Not a generic type
    assert not is_generic("hello")  # Not a generic type
