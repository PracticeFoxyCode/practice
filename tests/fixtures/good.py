import namespace.x.y
from . import something
from typing import Dict, List
from bad import behaviour  # foxylint-imports:ignore


def f():
    namespace.x.y.go()
