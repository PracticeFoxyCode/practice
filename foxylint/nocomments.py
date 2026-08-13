import re
import tokenize


class _AnalyzeFile:
    def __init__(self, file):
        self._file = file
        self._go()

    def _go(self):
        errors = []
        with open(self._file, 'rb') as f:
            for token in tokenize.tokenize(f.readline):
                if token.type != tokenize.COMMENT:
                    continue
                if self._acceptable(token):
                    continue
                errors.append({'line_number': token.start[0], 'line_content': token.line.strip()})
        ok = len(errors) == 0
        self._result = {'ok': ok, 'errors': errors}

    def _acceptable(self, token):
        if self._shebang(token):
            return True
        IGNORE_PATTERN = re.compile(r'foxylint-nocomments:ignore')
        return IGNORE_PATTERN.search(token.string) is not None

    def _shebang(self, token):
        return token.start[0] == 1 and token.string.startswith('#!')

    @property
    def result(self):
        return self._result


def analyze(files):
    analyses = {file: _AnalyzeFile(file).result for file in files}
    return analyses
