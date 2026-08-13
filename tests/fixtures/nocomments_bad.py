import logging


def f():
    # this is a banned comment
    logger = logging.getLogger(__name__)
    logger.info('hello')  # this trailing comment is also banned
    return logger
