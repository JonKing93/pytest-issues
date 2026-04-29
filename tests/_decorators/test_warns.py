import pytest

from pytest_issues._decorators.warns import deprecated_call, deprecates, warns


def check_missing_message(error, missing="missing message"):
    message = str(error.value)
    assert message == "No matching warnings were emitted"


def check_autofail(error):
    message = str(error.value)
    assert "No warning messages provided." in message


class TestWarns:
    def test_valid_type(_, warner, args, kwargs):
        @warns(RuntimeWarning, "some message A")
        def test():
            warner(*args, **kwargs)

        test()

    def test_valid_multiple_types(_, warner, args, kwargs):
        @warns((RuntimeWarning, UserWarning), "some message")
        def test():
            warner(*args, **kwargs)

        test()

    def test_invalid_type(_, warner, args, kwargs):
        @warns(UserWarning, "some message A")
        def test():
            warner(*args, **kwargs)

        with pytest.raises(match="DID NOT WARN. No warnings of type.*"):
            test()

    def test_invalid_multiple_types(_, warner, args, kwargs):
        @warns((UserWarning, FutureWarning), "some message")
        def test():
            warner(*args, **kwargs)

        with pytest.raises(match="DID NOT WARN. No warnings of type.*"):
            test()

    def test_valid_match(_, warner, args, kwargs):
        @warns(RuntimeWarning, "some message", match=".*final message C")
        def test():
            warner(*args, **kwargs)

        test()

    def test_invalid_match(_, warner, args, kwargs):
        @warns(RuntimeWarning, "some message", match="missing message")
        def test():
            warner(*args, **kwargs)

        with pytest.raises(
            match="DID NOT WARN. No warnings .* matching the regex were emitted"
        ):
            test()

    def test_invalid_message(_):

        with pytest.raises(TypeError) as error:
            warns(RuntimeWarning, 5)
        assert "error message[0] is not a string" in str(error.value)

    def test_invalid_message_double_none(_):
        with pytest.raises(TypeError) as einfo:
            warns(RuntimeWarning, None, None)
        assert str(einfo.value) == "error message[0] is not a string"

    def test_valid_message(_, warner, args, kwargs):
        @warns(RuntimeWarning, "some message A", "another message D", "final message C")
        def test():
            warner(*args, **kwargs)

        test()

    def test_missing_message(_, warner, args, kwargs):
        @warns(RuntimeWarning, "some message A", "missing message")
        def test():
            warner(*args, **kwargs)

        with pytest.raises(AssertionError) as einfo:
            test()
        check_missing_message(einfo)

    def test_autofail_message(_, warner, args, kwargs):
        @warns(RuntimeWarning)
        def test():
            warner(*args, **kwargs)

        with pytest.raises(AssertionError) as einfo:
            test()
        check_autofail(einfo)

    def test_disable_message(_, warner, args, kwargs):
        @warns(RuntimeWarning, None)
        def test():
            warner(*args, **kwargs)

        test()

    def test_format_message(_, warner, args, kwargs):
        @warns(RuntimeWarning, "{fixture1}")
        def test(fixture1, fixture2):
            warner(fixture1, fixture2, **kwargs)

        test(fixture1="some message A", fixture2="another message B")

    def test_no_format_message(_, warner, args, kwargs):
        @warns(RuntimeWarning, "{fixture1}", "{fixture2}", format=False)
        def test(fixture1, fixture2):
            warner(*args, **kwargs)

        with pytest.raises(AssertionError) as einfo:
            test(fixture1="some message A", fixture2="another message B")
        check_missing_message(einfo, missing="{fixture1}")

    def test_method_with_class_method(_, warner, args, kwargs):
        class TestClass:
            def amethod(_):
                assert True

            @warns(RuntimeWarning, "some message")
            def test(cls):
                cls.amethod()
                warner(*args, **kwargs)

        TestClass().test()

    def test_method_no_class_method(_, warner, args, kwargs):
        class TestClass:
            @warns(RuntimeWarning, "some message")
            def test(_):
                warner(*args, **kwargs)

        TestClass().test()


#####
# Deprecates
#####


class TestDeprecates:
    @pytest.mark.parametrize(
        "type", (DeprecationWarning, PendingDeprecationWarning, FutureWarning)
    )
    def test_passes(_, type, deprecator):
        @deprecates("some message A", "another message B")
        def test():
            deprecator(type)

        test()

    def test_fails(_, deprecator):
        @deprecates("some message A")
        def test():
            deprecator(RuntimeWarning)

        with pytest.raises(match="DID NOT WARN. No warnings of type .* were emitted"):
            test()


class TestDeprecatedCall:
    @pytest.mark.parametrize(
        "type", (DeprecationWarning, PendingDeprecationWarning, FutureWarning)
    )
    def test_passes(_, type, deprecator):
        @deprecated_call("some message A", "another message B")
        def test():
            deprecator(type)

        test()

    def test_fails(_, deprecator):
        @deprecated_call("some message A")
        def test():
            deprecator(RuntimeWarning)

        with pytest.raises(match="DID NOT WARN. No warnings of type .* were emitted"):
            test()
