from typing import Any, Callable, Union
from validate import is_callable, is_iterable, is_union, extract_types, validate, validate_iterable, validate_single


def assert_true(value: bool, message: str = ""):
    """
    Assert that `value` is True.

    Args:
        value (bool): Value to be checked.
        message (str, optional): Message to be displayed if `value` is False. Defaults to "".
    """
    if not value:
        raise AssertionError(message)


def assert_false(value: bool, message: str = ""):
    """
    Assert that `value` is False.

    Args:
        value (bool): Value to be checked.
        message (str, optional): Message to be displayed if `value` is True. Defaults to "".
    """
    if value:
        raise AssertionError(message)


def assert_equal(expected: Any, actual: Any, message: str = ""):
    """
    Assert that `expected` and `actual` are equal.

    Args:
        expected (Any): Expected value.
        actual (Any): Actual value.
        message (str, optional): Message to be displayed if `expected` and `actual` are not equal. Defaults to "".
    """
    if expected != actual:
        raise AssertionError(message)


def assert_not_equal(expected: Any, actual: Any, message: str = ""):
    """
    Assert that `expected` and `actual` are not equal.

    Args:
        expected (Any): Expected value.
        actual (Any): Actual value.
        message (str, optional): Message to be displayed if `expected` and `actual` are equal. Defaults to "".
    """
    if expected == actual:
        raise AssertionError(message)


def assert_raises(exception: type[Exception], func: Callable, *args, **kwargs):
    """
    Assert that `func` raises `exception`.

    Args:
        exception (type[Exception]): Exception to be raised.
        func (Callable): Function to be called.
        *args: Arguments to be passed to `func`.
        **kwargs: Keyword arguments to be passed to `func`.
    """
    try:
        func(*args, **kwargs)
    except exception:
        pass
    else:
        raise AssertionError(f"Expected '{exception}' to be raised.")


"""
Test is_callable.
"""
assert_true(is_callable(lambda: None))
assert_true(is_callable(print))
assert_false(is_callable(5))
assert_false(is_callable([1, 2, 3]))
assert_false(is_callable(False))

"""
Test is_iterable.
"""
assert_true(is_iterable([1, 2, 3]))
assert_true(is_iterable((1, 2, 3)))
assert_true(is_iterable({1, 2, 3}))
assert_true(is_iterable({1: 2, 3: 4}))
assert_true(is_iterable("abc"))
assert_true(is_iterable(range(3)))
assert_false(is_iterable(5))
assert_false(is_iterable(lambda: None))
assert_false(is_iterable(False))
assert_false(is_iterable(None))

"""
Test is_union.
"""
assert_true(is_union(Union[int, str]))
assert_true(is_union(Union[int, str, list[int]]))
assert_false(is_union(Union))
assert_false(is_union(int))
assert_false(is_union(str | int))
assert_false(is_union((list, int)))

"""
Test extract_types.    
"""
assert_equal(extract_types([int, str, float]), [int, str, float])
assert_equal(extract_types([int, str, list[int]]), [int, str, list[int]])
assert_equal(extract_types([int, [str, [bool, float, Callable]]]), [
             int, str, bool, float, Callable])
assert_equal(extract_types([int, [str, Union[bool, float, Callable]]]), [
             int, str, bool, float, Callable])

assert_raises(TypeError, extract_types, [int, str, 5])
assert_raises(TypeError, extract_types, int)

"""
Test validate_single.
"""
assert_true(validate_single(5, int))
assert_false(validate_single(5, str))

"""
Test validate.
"""
assert_true(validate(5, int))
assert_true(validate({1: 1, 2: 2}, dict))
assert_true(validate(5.0, float))
assert_true(validate(5, Union[int, float]))
assert_true(validate(5, [int, dict, float, bool]))
assert_true(validate(True, [int, dict, [float, [bool], str]]))

assert_raises(TypeError, validate, 5, str)
assert_raises(TypeError, validate, 5, Union[str, float])
assert_raises(TypeError, validate, 5, Union[str, float, dict])

"""
Test validate_iterable.
"""
assert_true(validate_iterable([1, 2, 3], [int]))
assert_true(validate_iterable([1, 2, 3, "Hello"], [int, str]))