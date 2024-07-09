# -*- coding: utf-8 -*-

from .logging import logger


class Config(object):
    def __init__(self):
        self.Module = None
        self.Version = None
        self.EndPoint = None
        self.Region = None
        self.SecretId = None
        self.SecretKey = None

    def _deserialize(self, config: dict):
        self.Module = config.get("Module")
        self.Version = config.get("Version")
        self.EndPoint = config.get("EndPoint")
        self.Region = config.get("Region")
        self.SecretId = config.get("SecretId")
        self.SecretKey = config.get("SecretKey")
        memeber_set = set(config.keys())
        for name, _ in vars(self).items():
            if name in memeber_set:
                memeber_set.remove(name)
        if len(memeber_set) > 0:
            logger.warning("%s fileds are useless." % ",".join(memeber_set))
