import logging
import sys
from typing import Optional, TextIO

DEFAULT_LOG_LEVEL = logging.WARNING
DEFAULT_LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"


def get_logger(name: Optional[str] = None) -> logging.Logger:
    logger = logging.getLogger(name or __name__)
    if not logger.handlers:
        logger.addHandler(logging.NullHandler())
    if logger.level == logging.NOTSET:
        logger.setLevel(DEFAULT_LOG_LEVEL)
    return logger


def setup_logging(
    level: int = DEFAULT_LOG_LEVEL,
    format: str = DEFAULT_LOG_FORMAT,
    stream: TextIO = sys.stderr,
    logger_name: Optional[str] = None,
) -> None:
    logger = get_logger(logger_name)
    logger.setLevel(level)

    # Remove all existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    handler = logging.StreamHandler(stream)
    handler.setFormatter(logging.Formatter(format))
    logger.addHandler(handler)

    # Prevent the log messages from being passed to the root logger
    logger.propagate = False


logger = get_logger()
