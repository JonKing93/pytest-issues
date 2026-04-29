import pytest

from pytest_issues._core import raises


def check_missing_message(error):
    assert "Error message did not contain expected string" in str(error.value)


#####
# Tests
#####


class TestMessageInNotes:
    def test(_, raiser, args, kwargs):
        try:
            raiser(*args, **kwargs)
        except Exception as e:
            error = e
        assert raises.message_in_notes("extra info D", error) == True
        assert raises.message_in_notes("extra info Z", error) == False


class TestCheckRaises:
    def test_invalid_type(_, raiser, args, kwargs):
        with pytest.raises(ValueError) as error:
            raises.check_raises(raiser, args, kwargs, TypeError, None, None, [], True)
        assert "Raises a ValueError" in str(error.value)

    def test_invalid_multiple_types(_, raiser, args, kwargs):
        with pytest.raises(ValueError) as error:
            raises.check_raises(
                raiser, args, kwargs, (TypeError, RuntimeError), None, None, [], False
            )
        assert "Raises a ValueError" in str(error.value)

    def test_valid_type(_, raiser, args, kwargs):
        raises.check_raises(raiser, args, kwargs, ValueError, None, None, [], False)

    def test_valid_multiple_types(_, raiser, args, kwargs):
        raises.check_raises(
            raiser, args, kwargs, (TypeError, ValueError), None, None, [], False
        )

    def test_invalid_match(_, raiser, args, kwargs):
        with pytest.raises(AssertionError) as error:
            raises.check_raises(
                raiser, args, kwargs, ValueError, "abc123", None, [], False
            )
        assert "Regex pattern did not match" in str(error.value)

    def test_valid_match(_, raiser, args, kwargs):
        raises.check_raises(
            raiser, args, kwargs, ValueError, "some message A", None, [], False
        )

    def test_invalid_check(_, raiser, args, kwargs, check_fails):
        with pytest.raises(AssertionError) as error:
            raises.check_raises(
                raiser, args, kwargs, ValueError, None, check_fails, [], False
            )
        message = str(error.value)
        assert "did not return True" in message

    def test_valid_check(_, raiser, args, kwargs, check_passes):
        raises.check_raises(
            raiser, args, kwargs, ValueError, None, check_passes, [], False
        )

    def test_valid_message(_, raiser, args, kwargs):
        raises.check_raises(
            raiser,
            args,
            kwargs,
            ValueError,
            None,
            None,
            ["some message A", "another message B", "final message C"],
            False,
        )

    def test_invalid_message(_, raiser, args, kwargs):
        with pytest.raises(AssertionError) as error:
            raises.check_raises(
                raiser,
                args,
                kwargs,
                ValueError,
                None,
                None,
                ["some message A", "missing message"],
                False,
            )
        check_missing_message(error)

    def test_valid_message_with_notes(_, raiser, args, kwargs):
        raises.check_raises(
            raiser,
            args,
            kwargs,
            ValueError,
            None,
            None,
            ["some message A", "extra info D", "note E", "another message B"],
            check_notes=True,
        )

    def test_invalid_message_with_notes(_, raiser, args, kwargs):
        with pytest.raises(AssertionError) as error:
            raises.check_raises(
                raiser,
                args,
                kwargs,
                ValueError,
                None,
                None,
                ["some message A", "note E", "missing message"],
                check_notes=True,
            )
        check_missing_message(error)

    def test_valid_check_notes_but_no_attr(_, raiser_no_notes, args, kwargs):
        raises.check_raises(
            raiser_no_notes,
            args,
            kwargs,
            ValueError,
            None,
            None,
            ["some message A"],
            check_notes=True,
        )

    def test_invalid_check_notes_but_no_attr(_, raiser_no_notes, args, kwargs):
        with pytest.raises(AssertionError) as error:
            raises.check_raises(
                raiser_no_notes,
                args,
                kwargs,
                ValueError,
                None,
                None,
                ["missing message"],
                check_notes=True,
            )
        check_missing_message(error)


class TestCheckTestRaises:
    def test_passed(_, raiser, args, kwargs):
        raises.check_test_raises(
            raiser,
            args,
            kwargs,
            ValueError,
            None,
            None,
            ("some message A", "message B"),
            check_notes=False,
            format=False,
        )

    def test_passed_format(_, raiser, args, kwargs):
        raises.check_test_raises(
            raiser,
            args,
            kwargs,
            ValueError,
            None,
            None,
            ("extra info {kwarg1}", "additional note {kwarg2}"),
            check_notes=True,
            format=True,
        )

    def test_failed(_, raiser, args, kwargs):
        with pytest.raises(ValueError) as error:
            raises.check_test_raises(
                raiser,
                args,
                kwargs,
                TypeError,
                None,
                None,
                ("A", "B"),
                check_notes=False,
                format=False,
            )
        assert "Raises a ValueError" in str(error.value)

    def test_missing_message(_, raiser, args, kwargs):
        with pytest.raises(AssertionError) as error:
            raises.check_test_raises(
                raiser,
                args,
                kwargs,
                ValueError,
                None,
                None,
                (),
                check_notes=False,
                format=False,
            )
        assert "No error messages provided" in str(error.value)

    def test_disabled_message_format(_, raiser, args, kwargs):
        raises.check_test_raises(
            raiser,
            args,
            kwargs,
            ValueError,
            None,
            None,
            None,
            check_notes=False,
            format=True,
        )

    def test_disabled_message_no_format(_, raiser, args, kwargs):
        raises.check_test_raises(
            raiser,
            args,
            kwargs,
            ValueError,
            None,
            None,
            None,
            check_notes=False,
            format=False,
        )
