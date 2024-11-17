import re


class _AnalyzeFile:
    def __init__(self, file):
        self._file = file
        self._go()

    def _go(self):
        self._result = {'ok': False, 'errors': []}
        return

    @property
    def result(self):
        return self._result


def analyze(files):
    analyses = {file: _AnalyzeFile(file).result for file in files}
    return analyses
