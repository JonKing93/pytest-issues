User Guide
==========

Import Decorators
-----------------

All decorators are imported from the :ref:`pytest_issues <pytest_issues>` namespace::

    from pytest_issues import raises


Validate Exception
------------------
To validate a test that should raise an exception, call the :ref:`@raises <pytest_issues.raises>` decorator with the expected type of exception, and one or more strings that should appear in the error message. Note that exception type subclasses will match the indicated type::

    from pytest_issues

    @raises(ValueError, 'some message A')
    def test():
        raise ValueError(
            'This test must raise a ValueError that contains some message A.'
        )

    @raises(TypeError, 'some message A', 'another message B', 'third message C')
    def test_multiple_messages():
        raise TypeError(
            "This test must raise a TypeError that contains some message A, "
            "another message B, and a third message C."
        )

    @raises(ValueError, 'some message')
    def test_fails_type():
        raise TypeError(
            "This test will fail because it does not raise a ValueError"
        )

    @raises(ValueError, 'missing message A')
    def test_fails_type():
        raise ValueError(
            "This test will fail because the raised exception's error message "
            "does not include the indicated string."
        )



Multiple Exception Types
------------------------
The exception type can also be a tuple of expected types. In this case, the raised exception must match at least one of the expected types::

    @raises((ValueError, TypeError), 'some message')
    def test():
        raise ValueError(
            'This test must raise either a ValueError or a TypeError'
        )


Auto-fail
---------
If you call :ref:`@raises <pytest_issues.raises>` without any error message strings, then the test will automatically fail, and the raised exception will be displayed in the pytest output. This can be useful for inspecting error messages while writing tests::

    @raises(ValueError)
    def test():
        raise ValueError(
            'This test will always fail, and the raised error message will be displayed '
            'in the pytest output.'
        )

.. tip::

    If you only want to validate the exception type (and not the message), then read the section on :ref:`disabling message validation <disable>` below.



.. _disable:

Disable Message Validation
--------------------------
If you want to validate an exception, but not the error message, you can disable message validation by setting the message to None::

    @raises(ValueError, None)
    def test():
        raise ValueError(
            "This test must raise a ValueError, but the error message "
            "does not matter"
        )

Alternatively, you can use the :ref:`@raises_ignore_message <pytest_issues.raises_ignore_message>` decorator, which is an alias for the above syntax::

    from pytest_issues import raises_ignore_message

    @raises_ignore_message(ValueError)
    def test():
        raise ValueError(
            "This test must raise a ValueError, but the error message "
            "does not matter"
        )

If you *never* want to validate the error message, consider using::

    from pytest_issues import raises_ignore_message as error

    @raises(ValueError)
    def test():
        raise ValueError(
            "This test must raise a ValueError, but the error message "
            "does not matter"
        )


Check Notes
-----------
By default, :ref:`@raises <pytest_issues.raises>` will only check the raised exception's string representation ``str(exception)`` for required error messages. Set ``check_notes = True`` to also check for messages in the exception's ``__notes__`` (when present)::

    @raises(ValueError, 'some message A', 'some note B')
    def test_will_fail():
        e = ValueError('some message A')
        e.add_note('some note B')
        raise e

    @raises(ValueError, 'some message A', 'some note B', check_notes=True)
    def test_will_pass():
        e = ValueError('some message A')
        e.add_note('some note B')
        raise e

You can also use the :ref:`raises_with_notes <pytest_issues.raises_with_notes>` decorator, which is an alias for the above syntax::

    from pytest_issues import raises_with_notes

    @raises_with_notes(ValueError, 'some message A', 'some note B')
    def test_will_pass():
        e = ValueError('some message A')
        e.add_note('some note B')
        raise e

If you *always* want to check for required messages in the exception's ``__notes__``, consider using::

    from pytest_issues import raises_with_notes as error

    @raises(ValueError, 'some message A', 'some note B')
    def test_will_pass():
        e = ValueError('some message A')
        e.add_note('some note B')
        raise e


Pytest Ecosystem
----------------
The ``raises`` decorator plays well with standard features of the pytest ecosystem, including test functions, test methods, `fixtures`_, and `parametrized tests`_::

    @raises(ValueError, 'some message')
    def test_function():
        raise ValueError('some message')

    class TestClass:
        @raises(ValueError, 'some message')
        def test_method(cls):
            cls.some_method()
            raise ValueError('some message')

    @raises(ValueError, 'some message')
    def test_fixtures(fixture1, fixture2):
        raise ValueError('some message')

    @raises(ValueError, 'some message')
    @pytest.mark.parametrize('my_param', (1,2,3))
    def test_parametrized(my_param):
        raise ValueError('some message')


.. _fixtures: https://docs.pytest.org/en/stable/explanation/fixtures.html

.. _parametrized tests: https://docs.pytest.org/en/stable/how-to/parametrize.html

Include Fixtures and Parameters in Messages
-------------------------------------------
By default, the provided error messages are formatted using ``str.format(**test_kwargs)`` prior to validation. This means that curly braces ``{}`` are treated as string placeholders, which you can use to inject pytest fixtures and parameters into expected error messages::

    @raises(ValueError, 'message with {param1} and {fixture2}')
    @pytest.mark.parametrize('param1', ('string1', 'string2', 'string3'))
    def test(param1, fixture1, fixture2):
        raise ValueError(f'some message with {param1} and {fixture2}')

Any string placeholder must match the name of one of the test's kwargs. For a test function, all arguments are treated as kwargs. For a test method, all arguments after the first are treated as kwargs::

    @raises(ValueError, 'message with {missing}')
    def test_fails_placeholder_not_kwarg(fixture1, fixture2):
        raise ValueError(
            "This test will fail because `missing` is not one of the test kwargs"
        )

    class TestClass:
        @raises(ValueError, 'message with {cls}')
        def test_fails_cls_not_kwarg(cls, fixture1, fixture2):
            raise ValueError(
                "This test will fail because `cls` is an arg, not a test kwarg"
            )

        @raises(ValueError, '{fixture1}')
        def test_passes(_, fixture1):
            raise ValueError(
                "This test will pass because {fixture1} is a kwarg"
            )


Disable Formatting
------------------

You can disable message formatting by setting ``format = False``. Use this to check for literal curly braces in test messages::

    @raises(ValueError, 'a message with {literal} curly braces', format=False)
    def test():
        raise ValueError(
            'The error message must include a message with {literal} curly braces'
        )

You can also use the :ref:`raises_no_format <pytest_issues.raises_no_format>` decorator, which is an alias for the above syntax::

    from pytest_issues import raises_no_format

    @raises_no_format(ValueError, 'a message with {literal} curly braces')
    def test():
        raise ValueError(
            'The error message must include a message with {literal} curly braces'
        )

If you *never* want to format messages, consider using::

    from pytest_issues import raises_no_format as error

    @raises(ValueError, 'a message with {literal} curly braces')
    def test():
        raise ValueError(
            'The error message must include a message with {literal} curly braces'
        )


Match Regex
-----------

The :ref:`@raises <pytest_issues.raises>` decorator inherits the ``match`` input from the `pytest.raises API`_. When provided, ``match`` should be a regular expression string, or compiled regular expression object. For the test to pass, the raised exception's string or ``__notes__`` must match this regex using `re.search`_::

    @raises(ValueError, None, match=some_regex)
    def test():
        raise ValueError(
            "This test must raise an exception whose string "
            "or __notes__ match the regex."
        )

.. note::

    The ``match`` input will **always** examine the exception's ``__notes__`` when available. Setting ``check_notes = False`` will not affect this behavior.


Custom Validator
----------------
The :ref:`@raises <pytest_issues.raises>` also inherits the ``check`` input from the `pytest.raises API`_. When provided, ``check`` should be a callable that accepts the raised exception as its only (positional) arg. If the callable returns True, then the exception is considered to have passed its validation. Anything else will cause the test to fail::

    @raises(ValueError, 'some message', check=some_validator)
    def test():
        raise ValueError(
            'Must raise an exception that (1) has some message, and '
            '(2) passes a custom validator.'
        )


Warnings
--------
You can also use the ``@warns`` decorator to check that a test issues an expected warning. The syntax is the same as for ``@raises``, but does not support the ``check`` and ``check_notes`` options::

    from pytest_issues import warns

    @warns(RuntimeWarning, "some warning message")
    def test():
        warnings.warn(
            "This test must raise some warning message",
            RuntimeWarning,
        )


Deprecations
------------
Finally, you can use ``@deprecates`` to check that a test issues a DeprecationWarning, PendingDeprecationWarning, or FutureWarning::

    from pytest_issues import deprecates

    @deprecates("some deprecation warning")
    def test():
        warnings.warn(
            "This test must issue some deprecation warning",
            DeprecationWarning,
        )

Note that ``@deprecates`` is strictly set to these three warning types. If you require more control over warning types (for example, to ensure a warning is specifically a DeprecationWarning rather than a FutureWarning), then use the ``@warns`` decorator instead.


.. _pytest.raises API: https://docs.pytest.org/en/stable/reference/reference.html#pytest-raises

.. _re.search: https://docs.python.org/3/library/re.html#re.search
