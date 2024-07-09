# -*- coding: utf-8 -*-


# Set up the basic logger configuration
import logging
from logging import NullHandler

logger = logging.getLogger(__name__)
logger.addHandler(NullHandler())
