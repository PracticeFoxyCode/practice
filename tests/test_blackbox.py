import pytest
import pathlib
import foxylint.imports
import foxylint.loggingcase
import foxylint.nocomments
import box

HERE = pathlib.Path(__file__).parent


@pytest.fixture
def files():
    good = str(HERE / 'fixtures' / 'good.py')
    bad = str(HERE / 'fixtures' / 'bad.py')
    nocomments_good = str(HERE / 'fixtures' / 'nocomments_good.py')
    nocomments_bad = str(HERE / 'fixtures' / 'nocomments_bad.py')
    return box.Box(good=good, bad=bad, nocomments_good=nocomments_good, nocomments_bad=nocomments_bad)


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


def test_nocomments(files):
    findings = foxylint.nocomments.analyze([files.nocomments_good, files.nocomments_bad])
    assert findings[files.nocomments_good]['ok'] is True
    assert len(findings[files.nocomments_good]['errors']) == 0
    assert findings[files.nocomments_bad]['ok'] is False
    assert len(findings[files.nocomments_bad]['errors']) == 2
