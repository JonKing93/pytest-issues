API Reference
=============

This page contains the full reference guide for using the ``pytest-issues`` API.

.. _pytest_issues:

.. list-table::
    :header-rows: 1

    * - Decorator
      - Description
    * - **Errors**
      -
    * - :ref:`raises <pytest_issues.raises>`
      - Ensure a test raises an expected exception
    * - :ref:`raises_with_notes <pytest_issues.raises_with_notes>`
      - Alias for ``@raises(..., check_notes=True)``
    * - :ref:`raises_no_format <pytest_issues.raises_no_format>`
      - Alias for ``@raises(..., format=False)``
    * - :ref:`raises_ignore_message <pytest_issues.raises_ignore_message>`
      - Alias for ``@raises(exception_type, None, *, ...)``
    * - **Warnings**
      -
    * - :ref:`warns <pytest_issues.warns>`
      - Ensure a test issues an expected warning
    * - :ref:`deprecates <pytest_issues.deprecates>`
      - Ensure a test issues an expected deprecation warning
    * - :ref:`deprecated_call <pytest_issues.deprecated_call>`
      - Alias for ``@deprecates``

----

Exceptions
----------

.. py:module:: pytest_issues

.. _pytest_issues.raises:

.. py:function:: raises(exception_type, *message, format=True, check_notes=False, match=None, check=None)
    :module: pytest_issues

    Decorator that checks that a pytest test raises an exception with expected characteristics.

    ::

        @raises(exception_type, *message)

    Requires a pytest test to raise an exception that matches the expected type (subclasses are considered matches). If the ``exception_type`` is a tuple of types, then the exception must match at least one of the types. The exception is also required to match any ``message`` strings in its string representation (``str(exception)``).

    For example::

        @raises(ValueError, 'some message A', 'another message B')
        def test():
            raise ValueError(
                'This test is required to raise a ValueError whose error message '
                'includes some message A, and another message B.
            )

    .. dropdown:: Auto-fail

        ::

            @raises(exception_type)

        If only an exception type is provided, then the test will fail, and the raised error message will be reported in the pytest output. This can be useful for inspecting error message appearance when writing tests.

        Example::

            @raises(ValueError)
            def test():
                raise ValueError(
                    'This test will fail and will report the error message of the raised exception'
                )

        Note that the auto-fail behavior can be disabled by setting ``message`` explicitly to None. This effectively disables error message validation for the test.

        Example::

            @raises(ValueError, None)
            def test():
                raise ValueError('This test will pass, and the error message is not examined')

        .. tip::

            You can also use the :ref:`raises_ignore_message <pytest_issues.raises_ignore_message>` decorator to disable error message validation.


    .. dropdown:: Advanced Messages

        ::

            @raises(..., *, format = False)
            @raises(..., *, check_notes = True)

        Additional options for validating error messages. By default, the ``@raises`` decorator will call ``str.format(**test_kwargs)`` on the provided error message strings. This allows the injection of pytest parameters and fixtures into tested error message strings, but causes curly braces ``{}`` to be interpreted as string formatting placeholders. Set ``format = False`` to disable the formatting step, retaining ``{}`` as literal string characters.

        Also by default, the decorator will only check for the provided error message strings in the exception's string representation (``str(exception)``). Set ``check_notes = True`` to also check for error message strings in the exception's ``__notes__`` (if present).

        Examples::

            @raises(ValueError, '{literal} braces', format=False)
            def test_no_format():
                raise ValueError(
                    'This test must raise a ValueError whose message includes {literal} braces'
                )

            @raises(ValueError, 'some message A', 'some note B', check_notes=True)
            def test_notes():
                e = ValueError('This test raises an error with some message')
                e.add_note('The exception also includes some note B')
                e.add_note('The notes will be examined when checking for error message strings')
                raise e


    .. dropdown:: pytest.raises API

        ::

            @raises(..., *, match)
            @raises(..., *, check)

        Options inherited from the `pytest.raises API`_. When provided, ``match`` should be a string containing a regular expression, or a regular expression object, that is tested against the string representation of the exception and its ``__notes__`` (if present) using `re.search`_. Note that ``match`` is not affected by the ``check_notes`` option, so is always tested against the exception's ``__notes__`` when possible.

        When provided, ``check`` should be a callable that will be called with the exception as a parameter after checking the ``exception_type`` and the ``match`` regex (if specified). If ``check`` returns True, then the exception is considered a match. Otherwise, the exception is treated as a failed match.

        Examples::

            @raises(ValueError, None, match='some message')
            def test_match():
                raise ValueError('The test must raise an exception whose error message matches the ``match`` regex.'')

            @raises(ValueError, 'some message', check=my_valdiation_function)
            def test_check():
                raise ValueError(
                    'The test must raise an exception with some message, and '
                    'the exception must also pass a custom validation function'
                )

    :Args:
        * **exception_type** (*type | tuple[type]*) -- A type or tuple of types that the raised exception should match. Subclasses are considered matches. If a tuple, the exception must match at least one of the indicated types.
        * **message** (*str | None*) -- One or more error message strings that should appear in the exception's string representation and optionally its notes. Set to None to explicitly disable error message validation.
        * **format** (*bool*) -- True (default) to apply ``str.format(**test_kwargs)`` to error message strings before validation, effectively treating curly braces ``{}`` as string placeholders. False to disable the formatting step, treating braces as literal characters.
        * **check_notes** (*bool*) -- True to also check for error message strings in the exception's ``__notes__``. False (default) to only check for messages in the exception's string representation.
        * **match** (*str | re.Pattern[str]*) -- An optional string regular expression or compiled regex object that will be matched against the exception's string representation and ``__notes__`` using `re.search`_.
        * **check** (*Callable*) -- A custom validation function that will be receive the raised exception as a parameter. Should return True if the exception passes validation.

    :Raises:
        * **TypeError** -- If an error message input is not a string
        * **AssertionError** -- If no error message string is provided
        * **AssertionError** -- If the raised exception does not pass the validation checks


.. _pytest_issues.raises_with_notes:

.. py:function:: raises_with_notes(exception_type, *message, format=True, match=None, check=None)

    Alias for ``@raises(..., check_notes=True)``. Useful if you frequently want to consider exception ``__notes__`` when validating error messages.

    For example::

        from pytest_issues import error_with_notes

        @raises_with_notes(ValueError, 'some message in a note')
        def test():
            e = ValueError('some message')
            e.add_note('some message in a note')
            raise e

    If you *always* want to consider exception notes, consider using::

        from pytest_issues import error_with_notes as error

        @raises(ValueError, 'some message in a note')
        def test():
            e = ValueError('some message')
            e.add_note('some message in a note')
            raise e


.. _pytest_issues.raises_no_format:

.. py:function:: raises_no_format(exception_type, *message, check_notes=False, match=None, check=None)

    Alias for ``@raises(..., format=False)``. Useful if you frequently want to check for error messages with literal curly braces ``{}``.

    For example::

        from pytest_issues import error_no_format

        @raises_no_format(ValueError, 'some message with {literal} braces')
        def test():
            raise ValueError('some message with {literal} braces')

    If you *never* want to format messages, consider using::

        from pytest_issues import error_no_format as error

        @raises(ValueError, 'some message with {literal} braces')
        def test():
            raise ValueError('some message with {literal} braces')


.. _pytest_issues.raises_ignore_message:

.. py:function:: raises_ignore_message(exception_type, *, match=None, check=None)

    Alias for ``@raises(exception_type, None, *, ...)``. Useful if you frequently want to disable error message validation.

    For example::

        from pytest_issues import error_ignore_message

        @raises_ignore_message(ValueError)
        def test():
            raise ValueError('The error message does not matter for this test')

    If you *never* want to validate error messages, consider using::

        from pytest_issues import error_ignore_message as error

        @raises(ValueError)
        def test():
            raise ValueError('The error message does not matter for this test')


Warnings
--------

.. _pytest_issues.warns:

.. py:function:: warns(warning_type, *message, format=True, match=None)
    :module: pytest_issues

    Decorator that checks a pytest test issues an expected warning

    ::

        @warns(warning_type, *message)

    Requires a pytest test to issue a warning that matches the expected type (subclasses are considered matches). If the ``warning_type`` is a tuple of types, then the warning must match at least one of the types. The warning is also required to include any provided ``message`` strings.

    For example::

        @warns(RuntimeWarning, 'some warning message A')
        def test():
            warnings.warn(
                "This test must issue some warning message A",
                RuntimeWarning,
            )

    .. dropdown:: Auto-fail

        ::

            @warns(warning_type)

        If only a warning type is provided, then the test will fail.

        Example::

            @warns(RuntimeWarning)
            def test():
                warnings.warn(
                    "This test will fail because no message is provided",
                    RuntimeWarning,
                )

        Note that the auto-fail behavior can be disabled by setting ``message`` explicitly to None. This effectively disables error message validation for the test.

        Example::

            @warns(RuntimeWarning, None)
            def test():
                warnings.warn("This test will pass", RuntimeWarning)


    .. dropdown:: Advanced Messages

        ::

            @raises(..., *, format = False)
            @raises(..., *, match)

        Additional options for validating warning messages. By default, the ``@warns`` decorator will call ``str.format(**test_kwargs)`` on the provided warning message strings. This allows the injection of pytest parameters and fixtures into tested warning message strings, but causes curly braces ``{}`` to be interpreted as string formatting placeholders. Set ``format = False`` to disable the formatting step, retaining ``{}`` as literal string characters.

        When provided, ``match`` should be a string containing a regular expression, or a regular expression object, that is tested against the warning message using `re.search`_.

        Examples::

            @warns(RuntimeWarning, '{literal} braces', format=False)
            def test_no_format():
                warnings.warn(
                    "This warning must include {literal} braces",
                    RuntimeWarning,
                )

            @warns(RuntimeWarning, None, match='some message')
            def test_match():
                warnings.warn(
                    "This test must issue a warning whose message matches the ``match`` regex",
                    RuntimeWarning,
                )


    :Args:
        * **warning_type** (*type | tuple[type]*) -- A type or tuple of types that the issued warning should match. Subclasses are considered matches. If a tuple, the warning must match at least one of the indicated types.
        * **message** (*str | None*) -- One or more warning message strings that should appear in the warning's string representation and optionally its notes. Set to None to explicitly disable warning message validation.
        * **format** (*bool*) -- True (default) to apply ``str.format(**test_kwargs)`` to warning message strings before validation, effectively treating curly braces ``{}`` as string placeholders. False to disable the formatting step, treating braces as literal characters.
        * **match** (*str | re.Pattern[str]*) -- An optional string regular expression or compiled regex object that will be matched against the warning message using `re.search`_.

    :Raises:
        * **TypeError** -- If a warning message input is not a string
        * **AssertionError** -- If no warning message string is provided
        * **AssertionError** -- If the issued warning does not pass the validation checks



.. _pytest_issues.deprecates:

.. py:function:: deprecates(*message, format=True, match=None)
    :module: pytest_issues

    A special case of :ref:`@warns <pytest_issues.warns>` that requires the warning type to be a DeprecationWarning, PendingDeprecationWarning, or FutureWarning.


.. _pytest_issues.deprecated_call:

.. py:function:: deprecated_call(*message, format=True, match=None)
    :module: pytest_issues

    An alias for :ref:`@deprecates <pytest_issues.deprecates>`.






.. _pytest.raises API: https://docs.pytest.org/en/stable/reference/reference.html#pytest-raises

.. _re.search: https://docs.python.org/3/library/re.html#re.search
