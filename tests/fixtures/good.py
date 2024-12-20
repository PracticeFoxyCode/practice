import logging
import namespace.x.y
from . import something
from .. import something_else
from ... import another_thing
from typing import Dict, List
from mylogging import logger
from bad import behaviour  # foxylint-imports:ignore


def f():
    namespace.x.y.go()
    logger = logging.getLogger(__name__)
    logging.info('hi there')
    logger.info('hello')
    # logger.info('I start with a capital but I am commented out')
    logging.info('I start with a capital, but I have a comment that allows this')  # foxylint-loggingcase:ignore
    logging.info('Another line starts with a capital, but I have a comment that allows this')  # foxylint-loggingcase:ignore
