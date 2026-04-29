import sys
from warnings import warn

import pytest

from pytest_issues import (
    deprecates,
    raises,
    raises_ignore_message,
    raises_with_notes,
    warns,
)


@pytest.fixture
def fixture1():
    return 1


@pytest.fixture
def fixture2():
    return 2


@pytest.fixture
def fixture_string():
    return "some string"


def add_notes(exc, notes):  # pragma: no cover
    if sys.version_info.minor < 11:
        exc.__notes__ = notes
    else:
        for note in notes:
            exc.add_note(note)


@raises(ValueError, "some message")
def test_function():
    raise ValueError("This test raises a ValueError with some message")


@raises((TypeError, ValueError), "some message")
def test_multiple_types():
    raise ValueError("This test raises a ValueError with some message")


@raises(ValueError, "some message A", "another message B", "final message C")
def test_multiple_messages():
    raise ValueError(
        "This test raises a ValueError with some message A, another message B, "
        "and a final message C"
    )


@raises(ValueError, None)
def test_disable_message():
    raise ValueError("Raises a ValueError, but the message doesn't matter")


@raises(ValueError, "some message")
def test_with_fixtures(fixture1, fixture2):
    raise ValueError("This test raises a ValueError with some message")


@raises(ValueError, "some message")
@pytest.mark.parametrize("param1,param2", ((1, "test1"), (2, "test2"), (3, "test3")))
def test_with_parameters(param1, param2):
    raise ValueError("Each of these runs raises a ValueError with some message")


@raises(ValueError, "some message that notes the value of {param2}")
@pytest.mark.parametrize("param1,param2", ((1, "test1"), (2, "test2"), (3, "test3")))
def test_parameter_in_message(param1, param2):
    raise ValueError(
        f"Each test raises a ValueError "
        f"with some message that notes the value of {param2}"
    )


@raises(ValueError, "message that contains {fixture_string}")
def test_fixture_in_message(fixture_string):
    raise ValueError(f"message that contains {fixture_string}")


@raises(ValueError, "{not a placeholder}", "{{}}", format=False)
def test_no_format():
    raise ValueError(
        "This error message includes some curly braces {{}} that should be tested "
        "literally {not a placeholder}."
    )


@raises(ValueError, "some message A", "note E", "extra info D", check_notes=True)
def test_check_notes():
    e = ValueError("Code raises an exception with some message A")
    add_notes(e, ["Here is some extra info D", "And an additional note E"])
    raise e


@pytest.mark.parametrize("param1,param2", (("test1", 1), ("test2", 2), ("test3", 3)))
@raises(
    (TypeError, ValueError, RuntimeError),
    "some message A",
    "another message with info on {param1}",
    "extra info D",
    "note E",
    check_notes=True,
)
def test_everything(param1, fixture1, param2, fixture2):
    e = ValueError(
        "Some complex error case that raises an exception with some message A, "
        f"and another message with info on {param1}"
    )
    add_notes(e, ["It has some extra info D", "and also note E"])
    raise e


class TestClass:
    def amethod(_):
        assert True

    @raises(ValueError, "some message")
    def test_method_with_class_method(cls):
        cls.amethod()
        raise ValueError("Raises an exception with some message")

    @raises(ValueError, "some message")
    def test_method_no_class_method(_):
        raise ValueError("Raises an exception with some message")

    @raises(ValueError, "some message A", "another message B")
    def test_method_with_fixtures(_, fixture1, fixture2):
        raise ValueError("Raises exception with some message A and another message B")

    @raises(ValueError, "some message")
    @pytest.mark.parametrize(
        "param1,param2", ((1, "test1"), (2, "test2"), (3, "test3"))
    )
    def test_method_with_parameters(_, param1, param2):
        raise ValueError("Each run raises an exception with some message")

    @pytest.mark.parametrize(
        "param1,param2", ((1, "test1"), (2, "test2"), (3, "test3"))
    )
    @raises(ValueError, "some message", "info on {param2}")
    def test_method_parametrize_message(_, param1, param2):
        raise ValueError(
            f"Each run raises an exception with some message and info on {param2}"
        )

    @pytest.mark.parametrize(
        "param1,param2", ((1, "test1"), (2, "test2"), (3, "test3"))
    )
    @raises(ValueError, "some message", "info on {param2}")
    def test_method_everything(cls, param1, param2, fixture1, fixture2):
        cls.amethod()
        raise ValueError(
            f"Each run raises an exception with some message and info on {param2}"
        )


@raises_with_notes(ValueError, "some message A", "extra info D", "note E")
def test_error_with_notes():
    e = ValueError("Raises exception with some message A")
    add_notes(e, ["some extra info D", "and also note E"])
    raise e


@raises_ignore_message(ValueError)
def test_error_no_message():
    raise ValueError("Raises an exception but the message doesn't matter")


@warns(RuntimeWarning, "some warning message")
def test_warns():
    warn("A warning with some warning message", RuntimeWarning)


@deprecates("some deprecation message")
def test_deprecates():
    warn("A warning with some deprecation message", DeprecationWarning)
