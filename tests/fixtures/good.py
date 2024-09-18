import namespace.x.y
from . import something
from .. import something_else
from ... import another_thing
from typing import Dict, List
from mylogging import logger
from bad import behaviour  # foxylint-imports:ignore


def f():
    namespace.x.y.go()
