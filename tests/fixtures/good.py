import namespace.x.y
from . import something
from bad import behaviour  # foxy-imports:ignore


def f():
    namespace.x.y.go()
