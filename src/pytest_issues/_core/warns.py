"""
Functions to check that a test issues an expected warning
----------
Functions:
    warning_is_match    - True if a warning matches all messages
    check_warns         - Checks a function call issues an expected warning
    check_test_warns    - Checks a test issues an expected warning
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from pytest_issues import _messages

if TYPE_CHECKING:
    from collections.abc import Callable

    from pytest_issues.typing import Match, Types


def warning_is_match(warning_message: str, messages: list[str]):
    "True if a warning matches all expected messages"
    return all(message in warning_message for message in messages)


def check_warns(
    func: Callable,
    func_args: tuple,
    func_kwargs: dict,
    warning_type: Types,
    match: Match | None,
    messages: list[str],
) -> None:
    "Checks a function call generates a warning with expected characteristics"

    # Make function call. Initial validation via pytest.warns
    with pytest.warns(warning_type, match=match) as warnings:
        func(*func_args, **func_kwargs)

    # Get the warnings that match the expected types
    warnings = [
        warning
        for warning in warnings.list
        if issubclass(warning.category, warning_type)
    ]

    # Search for a warning that matches all the message strings
    valid = False
    for warning in warnings:
        if warning_is_match(str(warning.message), messages):
            valid = True
            break

    # Assertion error if the test has no matching warning
    if not valid:
        raise AssertionError("No matching warnings were emitted")


def check_test_warns(
    func: Callable,
    func_args: tuple,
    func_kwargs: dict,
    warning_type: Types,
    match: Match | None,
    messages: tuple[str, ...] | None,
    format: bool,
) -> None:
    """
    Similar to check_warns, but aware of python testing environments. Refer to
    check_test_raises for more details.
    """

    # Parse messages and note whether required
    messages, require_messages = _messages.parse(messages, format, func_kwargs)

    # Validate the warnings
    check_warns(
        func,
        func_args,
        func_kwargs,
        warning_type,
        match,
        messages,
    )

    # Optionally require message checking
    if len(messages) == 0 and require_messages:
        raise AssertionError("No warning messages provided.")
