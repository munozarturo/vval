import pytest

from typing import Callable, Iterable, Union, List, Optional, Dict, Union
from vval.vval import (
    validate,
    validate_iterable,
    validate_option,
    validate_filter,
    is_union,
    is_iterable,
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


def test_validate_iterable_with_valid_elements():
    assert validate_iterable([1, 2, 3], int)
    assert validate_iterable(["a", "b", "c"], str)
    assert validate_iterable([1, "two", 3.0], Union[int, str, float])


def test_validate_iterable_with_mixed_elements():
    with pytest.raises(TypeError):
        validate_iterable([1, "two", None], int)


def test_validate_iterable_with_invalid_elements():
    with pytest.raises(TypeError):
        validate_iterable([1, 2, "three"], int)


def test_validate_iterable_with_callable_elements():
    assert validate_iterable([lambda x: x, print, sum], Callable)


def test_validate_iterable_with_empty_iterable():
    assert validate_iterable([], int)  # Assuming empty iterable is considered valid


def test_validate_iterable_with_non_iterable_input():
    with pytest.raises(TypeError):
        validate_iterable(123, int)


def test_validate_iterable_with_complex_types():
    assert validate_iterable([(1, "a"), (2, "b")], tuple)


def test_validate_option_with_valid_value():
    validate_option("apple", ["apple", "banana", "cherry"])
    validate_option(5, [1, 2, 3, 4, 5])


def test_validate_option_with_invalid_value():
    with pytest.raises(ValueError):
        validate_option("orange", ["apple", "banana", "cherry"])
    with pytest.raises(ValueError):
        validate_option(10, [1, 2, 3, 4, 5])


def test_validate_option_with_non_iterable_options():
    with pytest.raises(TypeError):
        validate_option("apple", "not an iterable")


def test_validate_option_with_empty_options():
    with pytest.raises(ValueError):
        validate_option("apple", [])


def test_validate_option_with_varied_types():
    validate_option(3.14, [1, "two", 3.14, (4, 5)])
    with pytest.raises(ValueError):
        validate_option((4, 5), [1, "two", 3.14])


def is_positive(num):
    return num > 0


def is_non_empty_string(value):
    return isinstance(value, str) and len(value) > 0


def test_validate_filter_with_valid_value():
    validate_filter(5, is_positive)
    validate_filter("hello", is_non_empty_string)


def test_validate_filter_with_invalid_value():
    with pytest.raises(ValueError):
        validate_filter(-3, is_positive)
    with pytest.raises(ValueError):
        validate_filter("", is_non_empty_string)


def test_validate_filter_with_non_callable_filter():
    with pytest.raises(TypeError):
        validate_filter(5, "not a callable")


def test_validate_filter_with_lambda():
    validate_filter(10, lambda x: x % 2 == 0)  # Even number
    with pytest.raises(ValueError):
        validate_filter(5, lambda x: x % 2 == 0)  # Odd number


def test_validate_filter_with_complex_callable():
    def complex_filter(value):
        if isinstance(value, int):
            return value % 3 == 0
        elif isinstance(value, str):
            return "a" in value
        return False

    validate_filter(9, complex_filter)
    validate_filter("apple", complex_filter)
    with pytest.raises(ValueError):
        validate_filter(10, complex_filter)
    with pytest.raises(ValueError):
        validate_filter("hello", complex_filter)
