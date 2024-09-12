import pathlib
import foxyy.imports

HERE = pathlib.Path(__file__).parent


def test_blackbox():
    good = str(HERE / 'fixtures' / 'good.py')
    bad = str(HERE / 'fixtures' / 'bad.py')
    files = [good, bad]
    findings = foxyy.imports.analyze(files)
    assert findings[good]['ok'] is True
    assert findings[bad]['ok'] is False
