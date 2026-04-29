from warnings import warn

import pytest

#####
# Raises
#####


@pytest.fixture
def raiser():
    def func(arg1, arg2, *, kwarg1, kwarg2):
        a = ValueError(
            f"Raises a ValueError with some message {arg1}, "
            f"another message {arg2}, and a final message C"
        )
        a.add_note(f"Here is some extra info {kwarg1}")
        a.add_note(f"And an additional note {kwarg2}")
        raise a

    return func


@pytest.fixture
def raiser_no_notes():
    def func(arg1, arg2, *, kwarg1, kwarg2):
        raise ValueError(
            f"Raises a ValueError with some message {arg1}, "
            f"another message {arg2}, and a final message C"
        )

    return func


@pytest.fixture
def args():
    return ("A", "B")


@pytest.fixture
def kwargs():
    return {"kwarg1": "D", "kwarg2": "E"}


@pytest.fixture
def check_passes():
    def check(exception):
        return True

    return check


@pytest.fixture
def check_fails():
    def check(exception):
        return False

    return check


#####
# Warnings
#####


@pytest.fixture
def deprecator():
    def func(type):
        warn("A warning message with some message A, and another message B", type)

    return func


@pytest.fixture
def warner():
    def func(arg1, arg2, *, kwarg1, kwarg2):
        message = (
            f"A warning message with some message {arg1}, "
            f"another message {kwarg1}, and a final message C"
        )
        warn(message, RuntimeWarning)

    return func


@pytest.fixture
def multiwarner():
    def func(arg1, arg2, *, kwarg1, kwarg2):
        message = (
            f"A warning message with some message {arg1}, "
            f"another message {kwarg1}, and a final message C"
        )
        warn(message, RuntimeWarning)
        message = (
            f"A warning message with some message {arg2}, "
            f"another message {kwarg2}, and a final message C"
        )
        warn(message, RuntimeWarning)
        message = (
            f"A warning message with some message {arg1}, "
            f"another message {kwarg2}, and a final message C"
        )
        warn(message, UserWarning)

    return func
