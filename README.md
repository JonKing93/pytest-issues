# pytest-issues

A decorator for testing exceptions with [pytest](https://docs.pytest.org/en/stable/index.html).


## About

The `pytest-issues` package provides decorators to ensure that pytest tests raise expected exceptions and warnings. Use the `@raises` decorator to check a test raises an expected exception, and `@warns` to check a test issues an expected warning. The decorators are built on the [pytest.raises][pytest.raises] and [pytest.warns](pytest.warns) context managers, and extends their functionality to allow validation of error messages using strings. (The baseline context managers require regular expressions to validate error messages).

Some motivations for the package include:

1. Testing error messages without needing regular expressions
2. Adding a marker to quickly identify tests that examine error states
3. Keeping the [action code][test anatomy] for exception tests at the same indent level as other tests

[pytest.raises]: https://docs.pytest.org/en/stable/how-to/assert.html#assertions-about-expected-exceptions
[test anatomy]: https://docs.pytest.org/en/stable/explanation/anatomy.html


## Examples

Require a test to raise an expected exception:

```python
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
```

Auto-fail and display the raised message in the pytest results (useful for examining error messages when writing tests):
```python
@raises(RuntimeError)
def test():
    raise RuntimeError(
        "Because @raises does not include any error message strings, "
        "this test will fail and will display the raised error message "
        "in the pytest output. Refer to the documentation for ways to "
        "disable auto-failing."
    )
```

Plays well with the pytest ecosystem:
```python
@raises(TypeError, 'some error message')
@pytest.mark.parametrize('parameter', (1,2,3))
def test_with_parameters(parameter):
    raise TypeError(
        'This test uses parameters, and should raise a TypeError with some error message'
    )

@raises(ValueError, 'some error message')
def test_with_fixtures(fixtureA, fixtureB):
    raise ValueError(
        'This test uses fixtures, and should raise a ValueError with some error message'
    )

class TestClass:
    @raises(RuntimeError, 'some error message')
    def test_that_is_a_method(cls):
        raise RuntimeError(
            'This test is a class method, and should raise a RuntimeError with some error message'
        )

@raises((ValueError, TypeError), 'some message', check=some_callable, match=some_regex)
def test_raises_api():
    raise ValueError(
        "This exception raised by this test must satisfy the `check` and `match` args "
        "from the pytest.raises API, and must raise a ValueError with some message."
    )
```

Inject parameters and fixtures into expected error messages:
```python
@raises(ValueError, 'message including {param1} and {fixture2}')
@pytest.mark.parametrize(
    'param1', ('some message A', 'some message B')
)
def test(param1, fixture1, fixture2):
    raise ValueError(
        f'This test should raise an exception that has a message '
        f'including {param1} and {fixture2}'
    )
```

Check for warning messages:
```python
import warnings
from pytest_issues import warns

@warns(RuntimeWarning, 'some warning message')
def test():
    warnings.warn(
        "This test must issue a RuntimeWarning that includes "
        "some warning message."
    )
```


## Documentation

You can find more detailed examples, a user guide, and a comprehensive API at the [project documentation](https://pytest-issues.readthedocs.io).


## Installation

**Requires**: Python 3.11+, pytest 8.4+

```
pip install pytest-issues
```

## Contributing / Feedback

We welcome contributions and feedback! To ask a question, suggest a feature, or report a bug, please open a new thread on our [Issues tracker](https://github.com/JonKing93/pytest-issues/issues). If you plan to contribute code, please read the contribution guide in the docs.


## License

MIT
