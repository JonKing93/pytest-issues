"""
Decorators for tests that should raise exceptions
----------
Main:
    raises                  - Requires a test to raise an expected exception

Aliases:
    raises_with_notes       - Alias for @raises(..., check_notes=True)
    raises_no_format        - Alias for @raises(..., format=False)
    raises_ignore_message   - Alias for @raises(type, None, ...)
"""

from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING

from pytest_issues import _messages
from pytest_issues._core.raises import check_test_raises

if TYPE_CHECKING:
    from collections.abc import Callable

    from pytest_issues.typing import Match, Types

#####
# Main
#####


def raises(
    exception_type: Types,
    *messages: str | None,
    format: bool = True,
    check_notes: bool = False,
    match: Match | None = None,
    check: Callable | None = None,
) -> None:
    """
    Decorator that requires a test to raise an expected exception

    @raises(exception_type, *messages)
    Requires the following test function to raise an exception that matches the
    indicated type (subclasses are considered a match). If `exception_type` is a
    tuple of types, then the exception is required to match at least one of the
    provided types. The exception is also required to include any provided error
    message strings in its string representation `str(exception)`.

    @raises(exception_type)
    @raises(exception_type, None)
    By default, raises an AssertionError if no error message strings are
    provided. The AssertionError will report the raised error message, which can
    be useful for examining error messages when writing tests. To disable this
    behavior (effectively disabling error message validation), set the message
    explicitly to None.

    @raises(..., *, format = False)
    @raises(..., *, check_notes = True)
    Additional options for validating error messages. By default, the decorator
    calls `messages.format(**test_kwargs)` on the provided error message
    strings. This allows the injection of pytest parameters into error messages,
    but means that curly braces {} will be interpreted as string formatting
    placeholders. Set format=False to disable this behavior, retaining {} as
    literal braces.

    By default, the decorator will only check for error message strings in the
    exception's string representation `str(exception)`. Set check_notes=True to
    also check for error message strings in the exception's __notes__
    (if present).

    @raises(..., *, match)
    @raises(..., *, check)
    Options inherited from the pytest.raises API. When provided, `match` should
    be a string containing a regular expression or a regular expression object.
    This regex will be tested against the string representation of the exception
    and its __notes__ (if present) using re.search. Note that that `match` is
    not affected by the `check_notes` option, so is always tested against the
    exception's __notes__ when possible.

    When provided, `check` should be a callable that will be called with the
    exception as a parameter after checking the `exception_type` and the `match`
    regex (if specified). If `check` returns True, then the exception is
    considered a match. Otherwise, the exception is treated as a failed match.

    Args:
        exception_type: The exception type that should be raised. If a tuple
            of types, then the raised exception must match at least one of the
            provided types
        *messages: Error message strings that must be contained in the
            exception's string representation (and optionally in its __notes__).
            At least one value must be provided - set to None to disable error
            message checking entirely.
        format: True (default) to call messages.format(**test_kwargs) on the
            provided error message strings. False to skip this step.
        check_notes: True to compare error message strings to both the
            exception's string representation and its __notes__. False (default)
            to only check the string representation.
        match: Regular expression string or compiled regex object that will be
            tested against the exception's string representation and __notes__
            using re.search
        check: Callable that will be called with the raised exception as a
            parameter. Should return True to indicate the exception is as
            expected.

    Raises:
        TypeError: If an error message input is neither a string, nor None
        AssertionError: If no error message input is provided
        AssertionError: If a raised exception does not match expected criteria
    """

    messages = _messages.validate(messages)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            check_test_raises(
                # function call
                func,
                args,
                kwargs,
                # pytest.raises api
                exception_type,
                match,
                check,
                # message checking
                messages,
                check_notes,
                format,
            )

        return wrapper

    return decorator


#####
# Aliases
#####


def raises_with_notes(
    exception_type: type | tuple[type],
    *message: str | None,
    format: bool = True,
    match: Match | None = None,
    check: Callable | None = None,
) -> None:
    "Alias for `@raises(..., *, check_notes=True)`"
    return raises(
        exception_type,
        *message,
        format=format,
        check_notes=True,
        match=match,
        check=check,
    )


def raises_no_format(
    exception_type: type | tuple[type],
    *message: str | None,
    check_notes: bool = False,
    match: Match | None = None,
    check: Callable | None = None,
) -> None:
    "Alias for @raises(..., *, format=False)"
    return raises(
        exception_type,
        *message,
        format=False,
        check_notes=check_notes,
        match=match,
        check=check,
    )


def raises_ignore_message(
    exception_type: type | tuple[type],
    *,
    match: Match | None = None,
    check: Callable | None = None,
) -> None:
    "Alias for `@raises(..., message=None)`"
    return raises(exception_type, None, match=match, check=check)
