import pytest

from typing import Callable, Iterable, Union, List, Optional, Dict, Union
from vval.vval import (
    validate,
    validate_iterable,
    validate_option,
    is_union,
    is_iterable,
    is_generic,
    is_callable,
    _extract_types,
    _validate_single,
    ValidationError,
)


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


def test_extract_types_simple_types():
    assert _extract_types([int, str]) == [int, str]
    assert _extract_types([List]) == [List]


def test_extract_types_union_types():
    assert _extract_types([Union[int, str]]) == [int, str]
    assert _extract_types([Union[List, Dict]]) == [List, Dict]


def test_extract_types_nested_iterables():
    assert _extract_types([[int, str], [bool]]) == [int, str, bool]
    assert _extract_types([Iterable[int], [Union[str, bytes]]]) == [
        Iterable[int],
        str,
        bytes,
    ]


def test_extract_types_with_callable():
    assert _extract_types([Callable, [int, Union[str, float]]]) == [
        Callable,
        int,
        str,
        float,
    ]


def test_extract_types_invalid_input():
    with pytest.raises(TypeError):
        _extract_types([123])  # Contains a non-type item

    with pytest.raises(TypeError):
        _extract_types(["string"])  # String is not a type


def test_validate_single_with_valid_types():
    assert _validate_single(5, int)
    assert _validate_single("hello", str)
    assert _validate_single([1, 2, 3], list)


def test_validate_single_with_callable():
    assert _validate_single(lambda x: x, Callable)
    assert not _validate_single(5, Callable)


def test_validate_single_with_invalid_types():
    assert not _validate_single("hello", int)
    assert not _validate_single(5, str)


def test_validate_single_with_generic_type():
    with pytest.raises(ValidationError):
        _validate_single([1, 2, 3], List[int])


def test_validate_single_with_invalid_type_argument():
    with pytest.raises(ValueError):
        _validate_single(5, "not a type")


def test_validate_single_with_callable_function():
    def example_function():
        pass

    assert _validate_single(example_function, Callable)


def test_validate_with_valid_types():
    assert validate(5, int)
    assert validate("hello", str)


def test_validate_with_union_types():
    assert validate(5, Union[int, str])
    assert validate("hello", Union[int, str])

    with pytest.raises(TypeError):
        validate(5.5, Union[int, str])


def test_validate_with_iterable_of_types():
    assert validate(5, [int, str])
    assert validate("hello", [int, str, List[str]])

    with pytest.raises(TypeError):
        validate(5.5, [int, str])


def test_validate_with_callable():
    assert validate(lambda x: x, Callable)

    with pytest.raises(TypeError):
        validate(5, Callable)


def test_validate_with_invalid_value():
    with pytest.raises(TypeError):
        validate(5, str)


def test_validate_with_invalid_type_argument():
    with pytest.raises(TypeError):
        validate(5, "not a type")


def test_validate_with_complex_cases():
    assert validate(5, [int, str, Callable])  # 5 is an int
    assert validate("hello", [int, str, Callable])  # "hello" is a str
    assert validate(lambda x: x, [int, str, Callable])  # lambda is a Callable

    with pytest.raises(TypeError):
        validate(5.5, [int, str, Callable])

    with pytest.raises(TypeError):
        validate([1, 2, 3], [int, str, Callable])


def test_validate_with_nested_iterables():
    assert validate(5, [[int, str], [bool]])

    with pytest.raises(TypeError):
        validate("hello", [[int, bool], [int]])
