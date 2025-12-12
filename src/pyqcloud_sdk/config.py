# -*- coding: utf-8 -*-

import os
from .logging import logger


class Config(object):
    """Configuration settings for the Tencent Cloud client."""

    # Environment variable names for credentials
    ENV_SECRET_ID = "TENCENTCLOUD_SECRET_ID"
    ENV_SECRET_KEY = "TENCENTCLOUD_SECRET_KEY"

    def __init__(self, auto_load_env: bool = False):
        """
        Initializes a Config object with default values.

        Args:
            auto_load_env (bool): Whether to automatically load credentials from environment variables.
                                Defaults to False for backward compatibility.
        """
        self.Module = None
        self.Version = None
        self.EndPoint = None
        self.Region = None
        self.SecretId = None
        self.SecretKey = None

        if auto_load_env:
            self.load_from_env()

    def load_from_env(self, id_env_name: str = None, key_env_name: str = None):
        """
        Loads SecretId and SecretKey from environment variables.

        Args:
            id_env_name (str, optional): Environment variable name for SecretId.
                                       Defaults to self.ENV_SECRET_ID.
            key_env_name (str, optional): Environment variable name for SecretKey.
                                        Defaults to self.ENV_SECRET_KEY.
        """
        id_env_name = id_env_name or self.ENV_SECRET_ID
        key_env_name = key_env_name or self.ENV_SECRET_KEY

        secret_id = os.environ.get(id_env_name)
        secret_key = os.environ.get(key_env_name)

        if secret_id:
            self.SecretId = secret_id
            logger.info(f"SecretId loaded from environment variable: {id_env_name}")

        if secret_key:
            self.SecretKey = secret_key
            logger.info(f"SecretKey loaded from environment variable: {key_env_name}")

        if not secret_id or not secret_key:
            logger.warning(f"Environment variables {id_env_name} or {key_env_name} are not set.")

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
