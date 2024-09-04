import unittest
import logging
import io
from contextlib import redirect_stdout

from pyqcloud_sdk.logging import setup_logging, get_logger  # Adjust import as needed


class TestLogging(unittest.TestCase):
    def setUp(self):
        # Reset the root logger before each test
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        logging.root.setLevel(logging.WARNING)

    def test_default_logging_setup(self):
        logger = get_logger("test_logger")
        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(logger.level, logging.WARNING)
        self.assertTrue(any(isinstance(h, logging.NullHandler) for h in logger.handlers))

    def test_custom_logging_setup(self):
        log_stream = io.StringIO()
        setup_logging(level=logging.DEBUG, stream=log_stream, logger_name="custom_logger")
        logger = get_logger("custom_logger")

        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")

        log_output = log_stream.getvalue()
        self.assertIn("DEBUG - custom_logger - Debug message", log_output)
        self.assertIn("INFO - custom_logger - Info message", log_output)
        self.assertIn("WARNING - custom_logger - Warning message", log_output)

    def test_log_levels(self):
        log_stream = io.StringIO()
        setup_logging(level=logging.WARNING, stream=log_stream)
        logger = get_logger()

        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")

        log_output = log_stream.getvalue()
        self.assertNotIn("Debug message", log_output)
        self.assertNotIn("Info message", log_output)
        self.assertIn("WARNING", log_output)
        self.assertIn("ERROR", log_output)

    def test_custom_format(self):
        log_stream = io.StringIO()
        custom_format = "%(levelname)s: %(message)s"
        setup_logging(level=logging.INFO, format=custom_format, stream=log_stream)
        logger = get_logger()

        logger.info("Test message")

        log_output = log_stream.getvalue()
        self.assertEqual(log_output.strip(), "INFO: Test message")

    def test_multiple_loggers(self):
        log_stream1 = io.StringIO()
        log_stream2 = io.StringIO()

        setup_logging(level=logging.INFO, stream=log_stream1, logger_name="logger1")
        setup_logging(level=logging.ERROR, stream=log_stream2, logger_name="logger2")

        logger1 = get_logger("logger1")
        logger2 = get_logger("logger2")

        logger1.info("Info from logger1")
        logger2.info("Info from logger2")
        logger2.error("Error from logger2")

        self.assertIn("Info from logger1", log_stream1.getvalue())
        self.assertNotIn("Info from logger2", log_stream2.getvalue())
        self.assertIn("Error from logger2", log_stream2.getvalue())


# if __name__ == "__main__":
#     unittest.main()
