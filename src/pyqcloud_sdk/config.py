# -*- coding: utf-8 -*-

from .logging import logger


class Config(object):
    """Configuration settings for the Tencent Cloud client."""

    def __init__(self):
        """Initializes a Config object with default values."""
        self.Module = None
        self.Version = None
        self.EndPoint = None
        self.Region = None
        self.SecretId = None
        self.SecretKey = None

    def _deserialize(self, config: dict):
        """
        Deserializes configuration settings from a dictionary.

        Args:
            config (dict): A dictionary containing configuration settings.
        """
        self.Module = config.get("Module")
        self.Version = config.get("Version")
        self.EndPoint = config.get("EndPoint")
        self.Region = config.get("Region")
        self.SecretId = config.get("SecretId")
        self.SecretKey = config.get("SecretKey")
        member_set = set(config.keys())
        for name, _ in vars(self).items():
            if name in member_set:
                member_set.remove(name)
        if len(member_set) > 0:
            logger.warning("%s fields are useless." % ",".join(member_set))
