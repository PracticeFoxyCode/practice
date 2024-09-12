import namespace.x.y
from . import something
from bad import behaviour  # foxxy-imports:ignore


def f():
    namespace.x.y.go()
