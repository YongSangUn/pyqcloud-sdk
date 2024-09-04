import logging
import sys

DEFAULT_LOG_LEVEL = logging.WARNING
DEFAULT_LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def setup_logging(level=DEFAULT_LOG_LEVEL, format=DEFAULT_LOG_FORMAT, stream=sys.stderr):
    """
    Configures the root logger.

    Args:
        level (int, optional): The logging level. Defaults to logging.WARNING.
        format (str, optional): The log message format. Defaults to DEFAULT_LOG_FORMAT.
        stream (TextIOWrapper, optional): The output stream. Defaults to sys.stderr.
    """
    handler = logging.StreamHandler(stream)
    handler.setFormatter(logging.Formatter(format))
    logging.basicConfig(level=level, handlers=[handler])
