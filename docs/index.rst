pytest-issues
=============

The pytest-issues package provides decorators that ensure pytest tests issue expected exceptions and warnings. The decorators are built on the `pytest.raises`_ and `pytest.warns`_ context managers, and extend their functionality to allow validation of error messages using strings. (The baseline context managers require regular expressions in order to validate error messages).



Examples
--------

Require a test to raise an expected exception::

    from pytest_issues import raises

    @raises(ValueError, "some message A", "another message B", "final message C")
    def test():
        raise ValueError(
            "This test must raise an ValueError whose error message "
            "must include some message A, another message B, and a final message C."
        )

    @raises((TypeError, ValueError), 'some message')
    def test_multiple_types():
        raise TypeError(
            "This test must raise either a TypeError or ValueError, "
            "and the error must include some message".
        )

Auto-fail and display the raised message in the pytest results (useful for examining error messages when writing tests)::

    @raises(RuntimeError)
    def test():
        raise RuntimeError(
            "Because @raises does not include any error message strings, "
            "this test will fail and will display the raised error message "
            "in the pytest output. Refer to the documentation for ways to "
            "disable auto-failing."
        )

Inject parameters and fixtures into expected error messages::

    @raises(ValueError, 'message including {param1} and {fixture2}')
    @pytest.mark.parametrize(
        'param1', ('some message A', 'some message B')
    )
    def test(param1, fixture1, fixture2):
        raise ValueError(
            f'This test should raise an exception that has a message '
            f'including {param1} and {fixture2}'
        )


Why use pytest-issues?
----------------------

Some motivations for the package include:

1. :ref:`Testing error messages without needing regular expressions <testing-error-messages>`
2. :ref:`Adding a marker to quickly identify tests that examine error states <identify-error-tests>`
3. :ref:`Keeping the action code for error tests at the same indent level as other tests <preserve-indent-level>`


.. _testing-error-messages:

Testing Error Messages
++++++++++++++++++++++
Although `pytest.raises`_ includes the ``match`` arg for validating error messages, its syntax relies on regular expressions. This can be difficult to use when validating error messages that include special regex characters, or when checking for multiple strings in the error message. By contrast, ``pytest_issues`` uses basic string matching to validate error messages, which is often simpler to use.

For example, compare the two syntaxes when checking for multiple strings in the error message:

.. tab-set::

    .. tab-item:: @raises

        ::

            @raises(ValueError, 'message A', 'message B', 'message C')
            def test():
                raise ValueError(
                    'This test must raise a ValueError with some message A, '
                    'another message B, and a third message C'
                )

    .. tab-item:: pytest.raises

        ::

            def test():
                match = "^(?=.*message A)(?=.*message B)(?=.*message C)""
                with pytest.raises(ValueError, match=match):
                    raise ValueError('message A, message B, message C')

Here, the regex is harder to read and *much* harder to code.


.. _identify-error-tests:

Identify Error Tests
++++++++++++++++++++
When working with large testing suites, it can be useful to quickly distinguish between tests that examine normal operation, and tests that examine error states. With ``pytest.raises``, this is only possible by inspecting the code itself. By contrast, ``@raises`` provides an immediate marker for tests that examine error states. Compare:

.. tab-set::

    .. tab-item:: @raises

        ::

            def test_1():
                pass

            @raises(ValueError, 'some message')
            def test_2():
                pass

            @raises(TypeError, 'another message')
            def test_3():
                pass

    .. tab-item:: pytest.raises

        ::

            def test_1():
                some_setup()
                some_action()
                some_cleanup()

            def test_2():
                some_setup()
                with pytest.raises(ValueError):
                    some_action()
                some_cleanup()

            def test_3():
                some_setup()
                with pytest.raises(TypeError):
                    some_action()
                some_cleanup()

Here, the ``@raises`` decorator allows quick identification of the tests that examine error states.


.. _preserve-indent-level:

Preserve Indent Level
+++++++++++++++++++++
A final motivation for ``pytest_issues`` concerns the indent level of action code for tests that examine error states. Ideally, tests should have their `action code`_ at the same indent level, regardless of whether they are testing error states or normal operation. This promotes parallel testing structures, and generally promotes test readability.

However, when using ``pytest.raises``, action code is typically run within a context manager, increasing its indent level. By contrast, ``@raises`` hides the context manager within the decorator, so the action code for error tests remains at the same indent level. Compare:

.. tab-set::

    .. tab-item:: @raises

        ::

            def test_normal():
                some_setup()
                some_action()
                some_cleanup()

            @raises(ValueError, 'some message')
            def test_failure():
                some_setup()
                some_action()

    .. tab-item:: pytest.raises

        ::

            def test_normal():
                some_setup()
                some_action()
                some_cleanup()

            def test_failure():
                some_setup()
                with pytest.raises(ValueError):
                    some_action()
                some_cleanup()

When using ``@raises``, the action code remains at the same indent level, regardless of test type.


.. _pytest: https://docs.pytest.org/en/stable/index.html

.. _pytest.raises: https://docs.pytest.org/en/stable/reference/reference.html#pytest-raises

.. _pytest.warns: https://docs.pytest.org/en/stable/reference/reference.html#pytest-warns

.. _action code: https://docs.pytest.org/en/stable/explanation/anatomy.html



.. toctree::
    :hidden:

    Introduction <self>
    Installation <install>
    Quickstart <quickstart>
    User Guide <user-guide>
    API Reference <api>
    Contributing <contributing>
    Release Notes <release-notes>
