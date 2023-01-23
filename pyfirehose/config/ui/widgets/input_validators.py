"""
SPDX-License-Identifier: MIT

Contains functions used for validating input types for forms.
"""

from collections.abc import Sequence

def integer_validator(value: str, **kwargs) -> bool: #pylint: disable=unused-argument
    """
    Checks that a string is a valid integer representation.

    Args:
        value: the string to test.
        kwargs: additional keyword arguments (unused, allow generic use of validators).

    Returns:
        A boolean indicating if the given string is a valid integer representation.
    """
    try:
        int(value)
    except ValueError:
        return True

    return False

def float_validator(value: str, **kwargs) -> bool: #pylint: disable=unused-argument
    """
    Checks that a string is a valid floating point representation.

    Args:
        value: the string to test.
        kwargs: additional keyword arguments (unused, allow generic use of validators).

    Returns:
        A boolean indicating if the given string is a valid floating point representation.
    """
    try:
        float(value)
    except ValueError:
        return True

    return False

def bool_validator(value: str, **kwargs) -> bool: #pylint: disable=unused-argument
    """
    Checks that a string is a valid boolean representation.

    Args:
        value: the string to test.
        kwargs: additional keyword arguments (unused, allow generic use of validators).

    Returns:
        A boolean indicating if the given string is a valid boolean representation.
    """
    return value.lower() in ['true', 'false']

def enum_validator(value: str, enum_values: Sequence[str]):
    """
    Checks that a string is a valid enum value from a given sequence of enum values.

    Args:
        value: the string to test.
        enum_values: the valid string values for the enum.

    Returns:
        A boolean indicating if the given string is a valid enum representation.
    """
    return value in enum_values

def string_validator(value: str, **kwargs): #pylint: disable=unused-argument
    """
    Placeholder validator for strings.

    Args:
        value: a string (unused).
        kwargs: additional keyword arguments (unused, allow generic use of validators).

    Returns:
        True
    """
    return True

def message_validator(value: str, **kwargs): #pylint: disable=unused-argument
    """
    Placeholder validator for messages.

    Args:
        value: a string (unused).
        kwargs: additional keyword arguments (unused, allow generic use of validators).

    Returns:
        True
    """
    return True
