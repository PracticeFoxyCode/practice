import re


class _AnalyzeFile:
    def __init__(self, file):
        self._file = file
        self._go()

    def _go(self):
        BAD_PATTERN = re.compile(r'from\s+(?P<namespace>\S)+\s+import')
        errors = []
        with open(self._file) as f:
            for line_number, line in enumerate(f, start=1):
                match = BAD_PATTERN.search(line)
                if match is not None:
                    namespace = match.group('namespace')
                    if self._acceptable(namespace):
                        continue
                    errors.append({'line_number': line_number, 'line_content': line.strip()})
        ok = len(errors) == 0
        self._result = {'ok': ok, 'errors': errors}

    def _acceptable(self, namespace):
        DOT = '.'
        return namespace == DOT

    @property
    def result(self):
        return self._result


def analyze(files):
    analyses = {file: _AnalyzeFile(file).result for file in files}
    return analyses
