import logging
from datetime import datetime
from pathlib import Path


def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    return logger
