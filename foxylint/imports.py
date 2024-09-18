import re


class _AnalyzeFile:
    def __init__(self, file, acceptable_patterns):
        self._file = file
        self._acceptable_patterns = acceptable_patterns
        self._go()

    def _go(self):
        BAD_PATTERN = re.compile(r'from\s+(?P<namespace>\S+)\s+import')
        errors = []
        with open(self._file) as f:
            for line_number, line in enumerate(f, start=1):
                match = BAD_PATTERN.search(line)
                if match is not None:
                    namespace = match.group('namespace')
                    if self._acceptable(namespace, line):
                        continue
                    errors.append({'line_number': line_number, 'line_content': line.strip()})
        ok = len(errors) == 0
        self._result = {'ok': ok, 'errors': errors}

    def _acceptable(self, namespace, line):
        for pattern in self._acceptable_patterns:
            regex = re.compile(pattern)
            match = regex.search(line)
            if match is not None:
                return True

        ACCEPTABLE_NAMESPACES = {'.', '..', '...', 'typing'}
        if namespace in ACCEPTABLE_NAMESPACES:
            return True

        IGNORE_PATTERN = re.compile(r'#\s*foxylint-imports:ignore\s*$')
        if IGNORE_PATTERN.search(line) is not None:
            return True

    @property
    def result(self):
        return self._result


def analyze(files, *, acceptable_patterns=None):
    if acceptable_patterns is None:
        acceptable_patterns = []
    analyses = {file: _AnalyzeFile(file, acceptable_patterns).result for file in files}
    return analyses
