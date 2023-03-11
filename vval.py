from varname import argname
from typing import Callable, Type, Union, Any, get_origin, get_args, Iterable
from types import UnionType
from typing_inspect import is_generic_type as is_generic


class Error(Exception):
    """Base class for exceptions in this module."""

    pass


class ValidationError(Error):
    """Base class for validation exceptions."""

    pass


def is_union(obj: Any) -> bool:
    """
    Check if `obj` is a Union.

    Args:
        obj (Any): Object to be checked.

    Returns:
        bool: Whether `obj` is a Union.
    """
    return get_origin(obj) is Union


def is_iterable(obj: Any) -> bool:
    """
    Check if `obj` is an iterable.

    Args:
        obj (Any): Object to be checked.

    Returns:
        bool: Whether `obj` is an iterable.
    """
    try:
        iter(obj)
    except TypeError:
        return False
    else:
        return True


def is_callable(obj: Any) -> bool:
    """
    Check if `obj` is callable.

    Args:
        obj (Any): Object to be checked.

    Returns:
        bool: Whether `obj` is callable.
    """
    return callable(obj)


def __extract_types(
    type_iter: Iterable[type | Type | UnionType | Iterable[type | Type | UnionType]],
) -> list[type | Type | UnionType]:
    """
    Extract all types from an iterable of types.

    Args:
        type_iter (Iterable[type | Type | UnionType | Iterable[type | Type | UnionType]]): Iterable of types.

    Returns:
        list[type | Type | UnionType]: List of types.

    Notes:
        If type_iter contains an iterable, it will be flattened. This includes `typing.Iterable`
        and any generic type built with `typing.Iterable` (e.g. Iterable[int], Iterable[str | list[str]], etc.).
        Due to this, just including `typing.Iterable` in `type_iter` will not work, and for this
        reason there is a function `validate_iterable` that can be used instead.
    """
    # validate iterable
    if not isinstance(type_iter, Iterable):
        raise TypeError(
            f"Expected 'Iterable' for `type_iter` got: '{type(type_iter)}'."
        )

    # list of types
    types: list[type | Type | UnionType] = []

    # iterate over type_iter
    for type_ in type_iter:
        # check if type_ is callable first because non generic use
        # raises errors; but can't be type checked
        if type_ == Callable:
            types.append(Callable)
        # if type_ is a single type then append it to the list
        elif isinstance(type_, type) or isinstance(type_, Type):
            types.append(type_)
        # if type_ is a Union get all union types
        elif is_union(type_):
            types += list(get_args(type_))
        # if type_ is an iterable, add all types to types
        elif is_iterable(type_):
            types += __extract_types(type_)
        else:
            raise TypeError(
                f"Expected 'type', 'Type', 'UnionType', or 'Iterable[type | Type | UnionType]' for `type_` got: '{type_}'."
            )

    # return types
    return types


def __validate_single(value: Any, type_: type | Type | Callable) -> bool:
    """
    Check if `value` is of type `type_`.

    Args:
        value (Any): Value to be checked.
        type_ (type | Type): Single type.

    Returns:
        bool: True if `value` is of type `type_`.
    """
    # check if type is generic, because generic types can't be validated
    if is_generic(type_):
        raise ValidationError(f"Can't validate generic type: '{type_}'.")

    # if type_ is callable check if it is callable
    if type_ == Callable:
        return is_callable(value)
    # if type_ is a single type then validate the single type
    elif isinstance(type_, Type) or isinstance(type_, type):
        return isinstance(value, type_)
    else:
        # else raise an error
        raise ValueError(f"Expected 'type' or 'Type' for `type_` got: '{type(type_)}'.")


def validate(
    value: Any,
    type_: type
    | Type
    | UnionType
    | Iterable[type | Type | UnionType | Iterable[type | Type | UnionType]],
) -> bool:
    """
    Validate that `value` is of type 'type_'.

    Args:
        value (Any): Value to be checked.
        type_ (type | Type | UnionType | Iterable[type | Type | UnionType]): Valid type(s).
        allow_none (bool, optional): Whether to allow 'None'. Defaults to False.

    Returns:
        bool: True if `value` is of type `type_`.

    Notes:
        If type_iter contains an iterable, it will be flattened. This includes `typing.Iterable`
        and any generic type built with `typing.Iterable` (e.g. Iterable[int], Iterable[str | list[str]], etc.).
        Due to this, just including `typing.Iterable` in `type_iter` will not work, and for this
        reason there is a function `validate_iterable` that can be used instead.
    """
    # list of allowed types
    allowed_types: list[type | Type] = []

    # if type_ is an iterable, add all types to allowed_types
    if is_iterable(type_):
        # if type_ is a Union get all union types
        if is_union(type_):
            allowed_types += list(get_args(type_))
        else:
            # extract types from type_
            allowed_types = __extract_types(type_)
    # if type_ is a single type then append it to the list
    elif (
        isinstance(type_, Type)
        or isinstance(type_, type)
        or isinstance(type_, Callable)
    ):
        allowed_types.append(type_)
    else:
        raise TypeError(
            f"Expected 'type', 'Type', 'UnionType', or 'Iterable[type | Type | UnionType]' for `type_` got: '{type_}'."
        )

    # check if value is of any of the allowed types
    for type_ in allowed_types:
        if __validate_single(value, type_):
            return True

    # if value is not of any of the allowed types raise an error
    _expected: str = ", ".join([str(type_.__name__) for type_ in allowed_types])

    try:
        var_name: str = argname("value")
    except Exception:
        var_name: str = "value"

    raise TypeError(
        f"Expected '{_expected}' for `{var_name}`, got: '{type(value).__name__}'."
    )


def validate_iterable(
    iter_: Iterable,
    type_: type | Type | UnionType | Iterable[type | Type | UnionType],
) -> bool:
    """
    Check if the contents of `iter_` are of type `type_`.

    Args:
        iter_ (Iterable): Iterable to be checked.
        type_ (type | Type | UnionType | Iterable[type  |  Type  |  UnionType]): type(s) allowed in `iter_`.

    Raises:
        TypeError: If `iter_` contains types not in `type_`.

    Returns:
        bool: True if the contents of `iter_` are of type `type_`.
    """
    # if iter_ is not an iterable raise an error
    if not is_iterable(iter_):
        raise TypeError(
            f"Expected 'Iterable' for `iter_`, got: '{type(iter_).__name__}'."
        )

    # validate every value in iter against type_
    for value in iter_:
        validate(value, type_)

    # return True
    return True


def validate_option(value: Any, options: Iterable[Any]):
    """
    Validate that `value` is one of the values in `options`.

    Args:
        value (Any): Value.
        options (Iterable[Any]): Iterable of values.

    Raises:
        ValueError: If `value` is not in `options`.
    """
    # if options is not an iterable raise an error
    if not isinstance(options, Iterable):
        raise TypeError(
            f"Expected 'Iterable' for `options`, got: '{type(options).__name__}'."
        )

    # raise an error if value is not in options
    if not value in options:
        raise ValueError(f"Expected one of {','.join(options)}, got: '{value}'.")
