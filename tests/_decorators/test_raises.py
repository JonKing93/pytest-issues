import pytest

from pytest_issues._decorators.raises import (
    raises,
    raises_ignore_message,
    raises_no_format,
    raises_with_notes,
)


def check_missing_message(error, missing="missing message"):
    message = str(error.value)
    assert message == (
        "Error message did not contain expected string.\n"
        "\n"
        "**Expected string**\n"
        f"{missing}\n"
        "\n"
        "**Actual message**\n"
        "Raises a ValueError with some message A, another message B, "
        "and a final message C"
    )


def check_autofail(error):
    message = str(error.value)
    assert message == (
        "No error messages provided\n"
        "\n"
        "**Raised message**\n"
        "Raises a ValueError with some message A, another message B, "
        "and a final message C"
    )


class TestRaises:
    def test_valid_type(_, raiser, args, kwargs):
        @raises(ValueError, "some message A")
        def test():
            raiser(*args, **kwargs)

        test()

    def test_valid_multiple_types(_, raiser, args, kwargs):
        @raises((TypeError, ValueError), "some message")
        def test():
            raiser(*args, **kwargs)

        test()

    def test_invalid_type(_, raiser, args, kwargs):
        @raises(TypeError, "some message")
        def test():
            raiser(*args, **kwargs)

        with pytest.raises(ValueError):
            test()

    def test_invalid_multiple_types(_, raiser, args, kwargs):
        @raises((TypeError, RuntimeError), "some message")
        def test():
            raiser(*args, **kwargs)

        with pytest.raises(ValueError):
            test()

    def test_valid_match(_, raiser, args, kwargs):
        @raises(ValueError, "some message", match="message B")
        def test():
            raiser(*args, **kwargs)

        test()

    def test_invalid_match(_, raiser, args, kwargs):
        @raises(ValueError, "some message", match="missing message")
        def test():
            raiser(*args, **kwargs)

        with pytest.raises(AssertionError):
            test()

    def test_valid_check(_, raiser, args, kwargs, check_passes):
        @raises(ValueError, "some message", check=check_passes)
        def test():
            raiser(*args, **kwargs)

        test()

    def test_invalid_check(_, raiser, args, kwargs, check_fails):
        @raises(ValueError, "some message", check=check_fails)
        def test():
            raiser(*args, **kwargs)

        with pytest.raises(AssertionError):
            test()

    def test_invalid_message(_):

        with pytest.raises(TypeError) as error:
            raises(ValueError, 5)
        assert "error message[0] is not a string" in str(error.value)

    def test_invalid_message_double_none(_):
        with pytest.raises(TypeError) as einfo:
            raises(ValueError, None, None)
        assert str(einfo.value) == "error message[0] is not a string"

    def test_valid_message(_, raiser, args, kwargs):
        @raises(ValueError, "some message A", "another message B", "final message C")
        def test():
            raiser(*args, **kwargs)

        test()

    def test_missing_message(_, raiser, args, kwargs):
        @raises(ValueError, "some message A", "missing message")
        def test():
            raiser(*args, **kwargs)

        with pytest.raises(AssertionError) as einfo:
            test()
        check_missing_message(einfo)

    def test_autofail_message(_, raiser, args, kwargs):
        @raises(ValueError)
        def test():
            raiser(*args, **kwargs)

        with pytest.raises(AssertionError) as einfo:
            test()
        check_autofail(einfo)

    def test_disable_message(_, raiser, args, kwargs):
        @raises(ValueError, None)
        def test():
            raiser(*args, **kwargs)

        test()

    def test_format_message(_, raiser, args, kwargs):
        @raises(ValueError, "{fixture1}", "{fixture2}")
        def test(fixture1, fixture2):
            raiser(*args, **kwargs)

        test(fixture1="some message A", fixture2="another message B")

    def test_no_format_message(_, raiser, args, kwargs):
        @raises(ValueError, "{fixture1}", "{fixture2}", format=False)
        def test(fixture1, fixture2):
            raiser(*args, **kwargs)

        with pytest.raises(AssertionError) as einfo:
            test(fixture1="some message A", fixture2="another message B")
        check_missing_message(einfo, missing="{fixture1}")

    def test_valid_with_notes(_, raiser, args, kwargs):
        @raises(ValueError, "some message A", "note E", check_notes=True)
        def test():
            raiser(*args, **kwargs)

        test()

    def test_invalid_with_notes(_, raiser, args, kwargs):
        @raises(
            ValueError, "some message A", "note E", "missing message", check_notes=True
        )
        def test():
            raiser(*args, **kwargs)

        with pytest.raises(AssertionError) as einfo:
            test()
        check_missing_message(einfo)

    def test_method_with_class_method(_, raiser, args, kwargs):
        class TestClass:
            def amethod(_):
                assert True

            @raises(ValueError, "some message")
            def test(cls):
                cls.amethod()
                raiser(*args, **kwargs)

        TestClass().test()

    def test_method_no_class_method(_, raiser, args, kwargs):
        class TestClass:
            @raises(ValueError, "some message")
            def test(_):
                raiser(*args, **kwargs)

        TestClass().test()


#####
# Aliases
#####


class TestRaisesWithNotes:
    def test_valid(_, raiser, args, kwargs):
        @raises_with_notes(ValueError, "some message A", "note E")
        def test():
            raiser(*args, **kwargs)

        test()

    def test_invalid(_, raiser, args, kwargs):
        @raises_with_notes(ValueError, "some message A", "note E", "missing message")
        def test():
            raiser(*args, **kwargs)

        with pytest.raises(AssertionError) as einfo:
            test()
        check_missing_message(einfo)


class TestRaisesNoFormat:
    def test_valid(_):
        @raises_no_format(ValueError, "{literal} curly braces")
        def test():
            raise ValueError("with {literal} curly braces")

        test()

    def test_invalid(_, raiser, args, kwargs):
        @raises_no_format(ValueError, "{fixture1} is literal")
        def test(fixture1):
            raise ValueError(f"with formatted info on {fixture1}")

        with pytest.raises(AssertionError) as einfo:
            test("some fixture")
        assert "{fixture1} is literal" in str(einfo.value)


class TestRaisesIgnoreMessage:
    def test_valid(_, raiser, args, kwargs):
        @raises_ignore_message(ValueError)
        def test():
            raiser(*args, **kwargs)

        test()

    def test_invalid(_, raiser, args, kwargs):
        @raises_ignore_message(RuntimeError)
        def test():
            raiser(*args, **kwargs)

        with pytest.raises(ValueError):
            test()
