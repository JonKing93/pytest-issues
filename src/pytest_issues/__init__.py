"""
Decorators that ensure tests issue expected exceptions or warnings
----------
This package provides decorators that check that pytest tests issue expected
exceptions or warnings. The decorators build off the pytest.raises and
pytest.warns context managers, and also add support for validating
error/warning messages using strings (rather than requiring regular
expressions).

Features:
* Validate error messages and warnings without needing regular expressions
* Quickly identify tests that examine error/warning states
* Action code remains at the same indent level as regular tests
----------
Main Decorators:
    raises      - Checks a test raises an expected exception
    warns       - Checks a test issues an expected warning
    deprecates  - Checks a test issues a deprecation warning

Aliases:
    raises_with_notes       - Alias for @raises(..., *, check_notes=True)
    raises_no_format        - Alias for @raises(..., *, format=False)
    raises_ignore_message   - Alias for @raises(exception_type, None, ...)
    deprecated_call         - Alias for @deprecates
"""

from pytest_issues._decorators.raises import (
    raises,
    raises_ignore_message,
    raises_no_format,
    raises_with_notes,
)
from pytest_issues._decorators.warns import deprecated_call, deprecates, warns

__all__ = [
    # Raises
    "raises",
    "raises_ignore_message",
    "raises_no_format",
    "raises_with_notes",
    # Warns
    "warns",
    "deprecates",
    "deprecated_call",
]
