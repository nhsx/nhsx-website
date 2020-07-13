# Testing

This site uses [Pytest](https://docs.pytest.org/en/latest/) for tests, running against an in-memory SQLite database for speed.

## Running tests

Most of the time, you will probably just want to run `script/test` to run all tests, but there are a few useful options you can pass to it.

* `script/test -x` - run all tests but stop on the first failure
* `script/test -s` - print stdout while the tests are running
* `script/test --pdb` - drop into a debugger when a test fails

These can be used in combination, most usefully `script/test -x --pdb` which will stop tests on the first failure and drop into the debugger.

## Coverage

To generate a coverage report, run `script/test --cov`. This will print the report to the screen at the end of the test run. You can then generate an HTML version with `coverage html` which outputs to `/app/htmlcov/` for viewing in a browser.

## Writing tests

It's worth getting know the pytest concept of [fixtures](https://docs.pytest.org/en/latest/reference.html#fixtures) - this lets you easily specify what objects your test will need in order to run.

At their most basic, you use them like this...

```
import pytest


@pytest.fixture(scope="function")
def some_object():
    return {
        "test": "foo",
        "test2": "bar"
    }


# A test function using the `some_object` fixture

def test_some_object(some_object):
    assert some_object is not None
    assert some_object['test'] == "foo"
    assert some_object['test2'] == "bar"

```

For passing complex model instances around as test fixtures, we use [Mixer](https://mixer.readthedocs.io/en/latest/). Mixer can automatically generate sane values for all your model's fields and return you a valid instance for testing.

### House Keeping

If your tests / fixtures are module specific, they should live in `modulename/tests/test_*`, otherwise there is a global tests folder too at `app/tests`.

If you add fixtures to a new location, you need to remember to tell pytest where to load them from. This is done at the top of `app/conftest.py` in the imports.

```
from tests.setup import setup
from tests.fixtures import *  # NOQA
```
