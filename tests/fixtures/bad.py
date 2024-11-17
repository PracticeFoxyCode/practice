import logging
from pathlib import Path
from bad import behavior


def main():
    logger = logging.getLogger(__name__)
    logger.info('I am also bad')
    logging.info('I start with a captial letter, that is why I am bad')
