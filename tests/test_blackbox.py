import pytest
import pathlib
import foxylint.imports
import foxylint.loggingcase
import box

HERE = pathlib.Path(__file__).parent


@pytest.fixture
def files():
    good = str(HERE / 'fixtures' / 'good.py')
    bad = str(HERE / 'fixtures' / 'bad.py')
    return box.Box(good=good, bad=bad)


def test_imports(files):
    LOGGING_PATTERN = 'from mylogging import logger'
    ACCEPTABLE_PATTERNS = [LOGGING_PATTERN]
    findings = foxylint.imports.analyze([files.good, files.bad], acceptable_patterns=ACCEPTABLE_PATTERNS)
    assert findings[files.good]['ok'] is True
    assert len(findings[files.good]['errors']) == 0
    assert findings[files.bad]['ok'] is False
    assert len(findings[files.bad]['errors']) == 2


def test_loggingcase(files):
    findings = foxylint.loggingcase.analyze([files.good, files.bad])
    assert findings[files.good]['ok'] is True
    assert len(findings[files.good]['errors']) == 0
    assert findings[files.bad]['ok'] is False
    assert len(findings[files.bad]['errors']) == 5
