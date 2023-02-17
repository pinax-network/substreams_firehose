"""
SPDX-License-Identifier: MIT

Contains functions used for validating input types for forms.
"""

from collections.abc import Sequence

from google.protobuf.message import DecodeError

from substreams_firehose.config.parser import load_substream_package

def integer_validator(value: str, **kwargs) -> bool: #pylint: disable=unused-argument
    """
    Checks that a string is a valid integer representation.

    Args:
        value: The string to test.
        kwargs: Additional keyword arguments (unused, allow generic use of validators).

    Returns:
        A boolean indicating if the given string is a valid integer representation.
    """
    try:
        int(value)
    except ValueError:
        return False

    return True

def float_validator(value: str, **kwargs) -> bool: #pylint: disable=unused-argument
    """
    Checks that a string is a valid floating point representation.

    Args:
        value: The string to test.
        kwargs: Additional keyword arguments (unused, allow generic use of validators).

    Returns:
        A boolean indicating if the given string is a valid floating point representation.
    """
    try:
        float(value)
    except ValueError:
        return False

    return True

def bool_validator(value: str, **kwargs) -> bool: #pylint: disable=unused-argument
    """
    Checks that a string is a valid boolean representation.

    Args:
        value: The string to test.
        kwargs: Additional keyword arguments (unused, allow generic use of validators).

    Returns:
        A boolean indicating if the given string is a valid boolean representation.
    """
    return value.lower() in ['true', 'false']

def enum_validator(value: str, enum_values: Sequence[str], **kwargs): #pylint: disable=unused-argument
    """
    Checks that a string is a valid enum value from a given sequence of enum values.

    Args:
        value: The string to test.
        enum_values: The valid string values for the enum.

    Returns:
        A boolean indicating if the given string is a valid enum representation.
    """
    return value in enum_values

def string_validator(value: str, **kwargs): #pylint: disable=unused-argument
    """
    Placeholder validator for strings.

    Args:
        value: A string (unused).
        kwargs: Additional keyword arguments (unused, allow generic use of validators).

    Returns:
        `True`
    """
    return True

def message_validator(value: str, **kwargs): #pylint: disable=unused-argument
    """
    Placeholder validator for generic messages.

    Args:
        value: A string (unused).
        kwargs: Additional keyword arguments (unused, allow generic use of validators).

    Returns:
        `True`
    """
    return True

def package_validator(value: str, **kwargs): #pylint: disable=unused-argument
    """
    Input validator for substream package files (.spkg).

    Args:
        value: The string to test.
        kwargs: Additional keyword arguments (unused, allow generic use of validators).

    Returns:
        A boolean indicating if the value is a valid package file.
    """
    try:
        return load_substream_package(value)
    except (DecodeError, FileNotFoundError, IsADirectoryError):
        return False

    return True
