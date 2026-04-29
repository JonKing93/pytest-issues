Quickstart
==========

Check that a pytest test raises an expected exception::

    from pytest_issues import raises

    @raises(ValueError, 'some message A', 'another message B', third message C')
    def test():
        raise ValueError(
            "This test must raise a ValueError that includes some message A, "
            "another message B, and a third message C."
        )

    @raises((ValueError, TypeError), 'some message')
    def test_multiple_types():
        raise TypeError(
            "This test must raise either a ValueError or a TypeError, "
            "and must report some message."
        )

----

Auto-fail to inspect error messages::

    @raises(ValueError)
    def test_autofail():
        raise ValueError(
            "The call to @raises does not include a message string, so this test "
            "will automatically fail and display the raised message in the "
            "pytest output"
        )

----

Inject fixtures and parameters into expected error messages::

    @raises(ValueError, 'some info about {param1} and {fixture2}')
    @pytest.mark.parametrize('param1', ('test1', 'test2', 'test3'))
    def test_format_message(param1, fixture1, fixture2):
        raise ValueError(
            f"Each test must raise an exception with some info about {param1} "
            f"and {fixture2}."
        )

----

Check a test issues a warning::

    from pytest_issues import warns
    import warnings

    @warns(RuntimeWarning, "some warning message")
    def test_warning():
        warnings.warn(
            "This test must issue some warning message",
            RuntimeWarning,
        )
