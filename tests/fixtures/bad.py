import logging
from pathlib import Path
from bad import behavior


def main():
    logger = logging.getLogger(__name__)
    logger.info('I am also bad')
    logging.info('I start with a captial letter, that is why I am bad')
    logging.info('Another line starts with a capital, this is bad')
    logging.info(f'An f-string with a capital letter is bad as well {3.0}')
    logging.info(r'An r-string with a capital letter is also bad')
