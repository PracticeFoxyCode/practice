#!/usr/bin/env python
import logging


def f():
    # this is explicitly allowed due to foxylint-nocomments:ignore
    logger = logging.getLogger(__name__)
    logger.info('hello')
    return logger  # foxylint-nocomments:ignore this trailing comment is an explicit exception
