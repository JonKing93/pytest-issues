"""
Decorators for tests that should issue warnings
----------
Decorators:
    warns           - Ensures a test issues an expected warning
    deprecates      - Ensures a test issues a deprecation warning
    deprecated_call - Alias for @deprecates
"""

from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING

from pytest_issues import _messages
from pytest_issues._core.warns import check_test_warns

if TYPE_CHECKING:
    from pytest_issues.typing import Match, Types


#####
# Main
#####


def warns(
    warning_type: Types,
    *messages: str | None,
    format: bool = True,
    match: Match | None = None,
) -> None:
    """
    Decorator that requires a test to issue an expected warning

    @warns(warning_type, *messages)
    Requires the following test function to issue a warning of the given type
    (subclasses are considered a match). If `warning_type` is a tuple of types,
    then the warning must match at least one of the given types. The warning is
    also required to include any provided message strings in the warning
    message.

    @warns(warning_type)
    @warns(warning_type, None)
    By default, raises an AssertionError if no warning message is provided. To
    disable this behavior (effectively disabling warning message validation),
    set the message explicitly to None.

    @warns(..., *, format=False)
    @warns(..., *, match)
    Additional options for validating warning messages. By default, the
    decorator calls `messages.format(**test_kwargs)` on the provided warning
    message strings. This allows the injection of pytest parameters into
    expected warning messages, but means that curly braces {} will be
    interpreted as string formatting placeholders. Set format=False to disable
    this behavior, treating {} as literal braces.

    Use `match` to providing a regular expression string or object that should
    be tested against the warning message using re.search. The test will fail
    if the warning message does not match this regex.

    Args:
        warning_type: A warning type that should be issued. If a tuple of types,
            then the raised exception must match at least one of the types
        *messages: Warning message strings that must be present in the warning
            message. By default, at least one message must be provided - set to
            None to disable this requirement.
        format: True (default) to call messages.format(**test_kwargs) on the
            provided warning message strings. False to skip this step
        match: Regular expression string or compiled regex object that will be
            tested against the warning message using re.search

    Raises:
        TypeError: If a warning message input is neither a string, nor None
        AssertionError: If no warning message input is provided
        AssertionError: If an issued warning does not match expected criteria
    """

    messages = _messages.validate(messages)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            check_test_warns(
                func,
                args,
                kwargs,
                warning_type,
                match,
                messages,
                format,
            )

        return wrapper

    return decorator


def deprecates(
    *messages: str | None,
    format: bool = True,
    match: Match | None = None,
) -> None:
    """
    Decorator that requires a test issues a deprecation warning.

    This decorator is intended to behave analogously to pytest.deprecated_call.
    As such, the decorator is simply an alias for:
    ```
    types = (DeprecationWarning, PendingDeprecationWarning, FutureWarning)
    @warns(types, ...)
    ```
    Note that you cannot set the warning type for this decorator, as they are
    fixed. If you want to check a specific one of these three warning types
    (for example, to check that the issued warning is exactly a
    PendingDeprecationWarning), then use @warns with the expected type instead.
    Aside from the warning type, all remaining arguments are the same as
    for @warns.
    """

    types = (DeprecationWarning, PendingDeprecationWarning, FutureWarning)
    return warns(
        types,
        *messages,
        format=format,
        match=match,
    )


def deprecated_call(
    *messages: str | None,
    format: bool = True,
    match: Match | None = None,
) -> None:
    """
    Alias for @deprecates
    """

    return deprecates(
        *messages,
        format=format,
        match=match,
    )
