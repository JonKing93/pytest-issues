import pytest

from pytest_issues import _messages


class TestValidate:
    def test_none(_):
        messages = (None,)
        output = _messages.validate(messages)
        assert output is None

    def test_valid(_):
        messages = ("some", "expected", "messages")
        output = _messages.validate(messages)
        assert output is messages

    def test_invalid(_):
        messages = ("message", 5, "another message")
        with pytest.raises(TypeError) as error:
            _messages.validate(messages)
        assert "error message[1] is not a string" in str(error.value)


class TestParse:
    def test_none(_):
        messages, required = _messages.parse(None, True, {"some": "kwarg"})
        assert messages == []
        assert required == False

    def test_basic(_):
        messages = ("some", "messages")
        messages, required = _messages.parse(messages, True, {})
        assert messages == ["some", "messages"]
        assert required == True

    def test_format(_):
        messages = ("test {arg}", "Another {test} and {arg}")
        messages, required = _messages.parse(
            messages, True, {"test": "A", "arg": "B", "extra": "C"}
        )
        assert messages == ["test B", "Another A and B"]
        assert required == True

    def test_no_format(_):
        messages = ("test {arg}", "Another {test} and {arg}")
        messages, required = _messages.parse(
            messages, False, {"test": "A", "arg": "B", "extra": "C"}
        )
        assert messages == ["test {arg}", "Another {test} and {arg}"]
        assert required == True
