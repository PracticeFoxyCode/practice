import pathlib
import foxylint.imports

HERE = pathlib.Path(__file__).parent


def test_blackbox():
    good = str(HERE / 'fixtures' / 'good.py')
    bad = str(HERE / 'fixtures' / 'bad.py')
    files = [good, bad]
    LOGGING_PATTERN = 'from mylogging import logger'
    ACCEPTABLE_PATTERNS = [LOGGING_PATTERN]
    findings = foxylint.imports.analyze(files, acceptable_patterns=ACCEPTABLE_PATTERNS)
    assert findings[good]['ok'] is True
    assert findings[bad]['ok'] is False
