import re


class _AnalyzeFile:
    def __init__(self, file):
        self._file = file
        self._go()

    def _go(self):
        BAD_PATTERN = re.compile(r"""(logging|logger)\.(info|warning|error|debug|critical)\(["'][A-Z]""")
        errors = []
        with open(self._file) as f:
            for line_number, line in enumerate(f, start=1):
                match = BAD_PATTERN.search(line)
                if match is not None:
                    if self._acceptable(line):
                        continue
                    errors.append({'line_number': line_number, 'line_content': line.strip()})
        ok = len(errors) == 0
        self._result = {'ok': ok, 'errors': errors}

    def _acceptable(self, line):
        if self._comment(line):
            return True
        IGNORE_PATTERN = re.compile(r'#\s*foxylint-loggingcase:ignore\s*$')
        return IGNORE_PATTERN.search(line) is not None

    def _comment(self, line):
        return line.strip().startswith('#')

    @property
    def result(self):
        return self._result


def analyze(files):
    analyses = {file: _AnalyzeFile(file).result for file in files}
    return analyses
