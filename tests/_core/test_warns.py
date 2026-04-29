import pytest

from pytest_issues._core import warns

#####
# Testing Setup
#####


@pytest.fixture
def args():
    return ("A", "B")


@pytest.fixture
def kwargs():
    return {"kwarg1": "D", "kwarg2": "E"}


class TestWarningIsMatch:
    def test_match(_):
        messages = ["some info A", "more info B"]
        warning_message = "A warning message with some info A, and more info B"
        assert warns.warning_is_match(warning_message, messages) == True

    def test_not_match(_):
        messages = ["some info A", "more info B", "extra info C"]
        warning_message = "A warning message with some info A, and more info B"
        assert warns.warning_is_match(warning_message, messages) == False


class TestCheckWarns:
    def test_invalid_type(_, warner, args, kwargs):
        with pytest.raises(match="DID NOT WARN"):
            warns.check_warns(warner, args, kwargs, UserWarning, None, [])

    def test_invalid_multiple_types(_, warner, args, kwargs):
        with pytest.raises(match="DID NOT WARN"):
            warns.check_warns(
                warner, args, kwargs, (UserWarning, FutureWarning), None, []
            )

    def test_valid_type(_, warner, args, kwargs):
        warns.check_warns(warner, args, kwargs, RuntimeWarning, None, [])

    def test_valid_multiple_types(_, warner, args, kwargs):
        warns.check_warns(warner, args, kwargs, (UserWarning, RuntimeWarning), None, [])

    def test_invalid_match(_, warner, args, kwargs):
        with pytest.raises(match="DID NOT WARN") as error:
            warns.check_warns(warner, args, kwargs, RuntimeWarning, "abc123", [])
        expected = ("No warnings", "matching the regex were emitted")
        for message in expected:
            assert message in str(error.value)

    def test_valid_match(_, warner, args, kwargs):
        warns.check_warns(warner, args, kwargs, RuntimeWarning, "some message A", [])

    def test_valid_message(_, warner, args, kwargs):
        warns.check_warns(
            warner,
            args,
            kwargs,
            RuntimeWarning,
            None,
            ["some message A", "another message D"],
        )

    def test_invalid_message(_, warner, args, kwargs):
        with pytest.raises(AssertionError) as error:
            warns.check_warns(
                warner,
                args,
                kwargs,
                RuntimeWarning,
                None,
                ["some message A", "more info B"],
            )
        assert "No matching warnings were emitted" in str(error.value)

    def test_pass_multiple_warnings(_, multiwarner, args, kwargs):
        warns.check_warns(
            multiwarner,
            args,
            kwargs,
            RuntimeWarning,
            None,
            ["some message B", "another message E"],
        )

    def test_message_but_not_type(_, multiwarner, args, kwargs):
        with pytest.raises(AssertionError) as error:
            warns.check_warns(
                multiwarner,
                args,
                kwargs,
                RuntimeWarning,
                None,
                ["some message A", "another message E"],
            )
        assert "No matching warnings were emitted" in str(error.value)

    def test_no_complete_match(_, multiwarner, args, kwargs):
        with pytest.raises(AssertionError) as error:
            warns.check_warns(
                multiwarner,
                args,
                kwargs,
                RuntimeWarning,
                None,
                ["some message A", "some message B"],
            )
        assert "No matching warnings were emitted" in str(error.value)


class TestCheckTestWarns:
    def test_passed(_, warner, args, kwargs):
        warns.check_test_warns(
            warner,
            args,
            kwargs,
            RuntimeWarning,
            None,
            ("some message A", "another message D"),
            format=False,
        )

    def test_passed_format(_, warner, args, kwargs):
        warns.check_test_warns(
            warner,
            args,
            kwargs,
            RuntimeWarning,
            None,
            ("some message A", "another message {kwarg1}"),
            format=True,
        )

    def test_failed(_, warner, args, kwargs):
        with pytest.raises(match="DID NOT WARN"):
            warns.check_test_warns(
                warner,
                args,
                kwargs,
                UserWarning,
                None,
                ("A", "B"),
                format=False,
            )

    def test_missing_message(_, warner, args, kwargs):
        with pytest.raises(AssertionError) as error:
            warns.check_test_warns(
                warner,
                args,
                kwargs,
                RuntimeWarning,
                None,
                (),
                format=False,
            )
        assert "No warning messages provided" in str(error.value)

    def test_disabled_message_format(_, warner, args, kwargs):
        warns.check_test_warns(
            warner,
            args,
            kwargs,
            RuntimeWarning,
            None,
            None,
            format=True,
        )

    def test_disabled_message_no_format(_, warner, args, kwargs):
        warns.check_test_warns(
            warner,
            args,
            kwargs,
            RuntimeWarning,
            None,
            None,
            format=False,
        )
