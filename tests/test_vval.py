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
    assert not is_generic(Union[str, int])
    assert not is_generic(int)  # Not a generic type
    assert not is_generic(3.14)  # Not a generic type
    assert not is_generic("hello")  # Not a generic type


def test_is_callable():
    assert is_callable(lambda x: x)  # Lambdas are callable
    assert is_callable(print)  # Built-in functions are callable
    assert is_callable(is_callable)  # The function itself is callable

    class MyClass:
        def __call__(self):
            pass

    assert is_callable(MyClass)  # Classes are callable
    assert is_callable(MyClass())  # Instances with a __call__ method are callable

    assert not is_callable(42)  # Integers are not callable
    assert not is_callable(None)  # None is not callable
    assert not is_callable([1, 2, 3])  # Lists are not callable
