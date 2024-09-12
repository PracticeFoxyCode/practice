import re


class _AnalyzeFile:
    def __init__(self, file):
        self._file = file
        self._go()

    def _go(self):
        BAD_PATTERN = re.compile(r'from\s+\S+\s+import', re.MULTILINE)
        with open(self._file) as f:
            text = f.read()
            errors = BAD_PATTERN.findall(text)
            ok = len(errors) == 0
            self._result = {'ok': ok, 'errors': errors}

    @property
    def result(self):
        return self._result


def enforce(files):
    results = {file: _AnalyzeFile(file).result for file in files}
    return results
