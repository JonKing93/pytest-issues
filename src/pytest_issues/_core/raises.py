"""
Functions to check that a test raises an expected exception
----------
Functions:
    message_in_notes    - True if a message is in an Exception's notes
    check_raises        - Checks a function call raises an expected Exception
    check_test_raises   - Checks a test raises an expected Exception
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from pytest_issues import _messages

if TYPE_CHECKING:
    from collections.abc import Callable

    from pytest_issues.typing import Match, Types


def message_in_notes(message: str, exception: Exception) -> bool:
    "True if a message is in an exception's notes"

    return any(message in note for note in exception.__notes__)


def check_raises(
    # Function call
    func: Callable,
    func_args: tuple,
    func_kwargs: dict,
    # Pytest API
    exception_type: Types,
    match: Match | None,
    check: Callable | None,
    # pytest-issues
    messages: list[str],
    check_notes: bool,
) -> Exception:
    """
    Checks a function call generates an expected Exception. Raises an
    AssertionError if the exception is not as expected.
    """

    # Make function call. Initial exception validation via pytest.raises
    with pytest.raises(exception_type, match=match, check=check) as error:
        func(*func_args, **func_kwargs)

    # Extract error message from ExceptionInfo. Also record whether to check
    # for messages in notes
    exception = error.value
    raised_message = str(exception)
    check_notes = check_notes and hasattr(exception, "__notes__")

    # Check the error message contains expected message strings
    for message in messages:
        valid = (message in raised_message) or (
            check_notes and message_in_notes(message, exception)
        )
        if not valid:
            raise AssertionError(
                f"Error message did not contain expected string."
                f"\n\n"
                f"**Expected string**\n{message}"
                f"\n\n"
                f"**Actual message**\n{raised_message}"
            )
    return exception


def check_test_raises(
    # Function call
    func: Callable,
    func_args: tuple,
    func_kwargs: dict,
    # Pytest API
    exception_type: Types,
    match: Match | None,
    check: Callable | None,
    # pytest-error
    messages: tuple[str, ...] | None,
    check_notes: bool,
    format: bool,
) -> None:
    """
    This function is similar to check_raises, but is designed to be aware of
    pytest testing environments. As such, the function will call str.format on
    message strings, allowing injection of pytest parameters into expected error
    messages (set format=False to disable this behavior).

    The function also implements the opinion that exception tests should usually
    examine the error message. If the test does not include an expected error
    message (indicated by `message` being an empty list), raises an
    AssertionError that includes any raised error message. This behavior can be
    disabled by setting `message` explicitly to None.
    """

    # Parse messages and note whether required
    messages, require_messages = _messages.parse(messages, format, func_kwargs)

    # Validate the exception
    exception = check_raises(
        func,
        func_args,
        func_kwargs,
        exception_type,
        match,
        check,
        messages,
        check_notes,
    )

    # Optionally require message checking
    if len(messages) == 0 and require_messages:
        raise AssertionError(
            f"No error messages provided\n\n**Raised message**\n{str(exception)}"
        )
