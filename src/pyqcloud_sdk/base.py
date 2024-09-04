# -*- coding: utf-8 -*-


import os
from time import sleep
from typing import Any

from tencentcloud.common.common_client import CommonClient
from tencentcloud.common.credential import Credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile

from .config import Config
from .exceptions import AuthenticationError, ClientError, ConfigError
from .logging import logger


class QcloudBase:
    def __init__(self, service_config: dict):
        self.config = Config()
        self.config._deserialize(service_config)
        # if not self.config.Region:
        #     raise ConfigError("Parameter 'region' is None")

    def set_region(self, region: str):
        self.config.Region = region
        logger.info(f"Region set to: {region}")

    def set_secret_key(self, secretKey: str):
        self.config.SecretKey = secretKey
        logger.info("SecretKey set.")

    def set_secret_id(self, secretId: str):
        self.config.SecretId = secretId
        logger.info("SecretId set.")

    def _try_set_secret_from_env(
        self,
        id_env_name: str = "TENCENTCLOUD_SECRET_ID",
        key_env_name: str = "TENCENTCLOUD_SECRET_KEY",
    ) -> bool:
        secret_id = os.environ.get(id_env_name)
        secret_key = os.environ.get(key_env_name)
        if not secret_id or not secret_key:
            logger.warning("SecretId or SecretKey environment variable is not set.")
            return False

        self.config.SecretId, self.config.SecretKey = secret_id, secret_key
        logger.info("Secrets set from environment variables.")
        return True

    def new_client(self) -> CommonClient:
        if not self.config.SecretId or not self.config.SecretKey:
            logger.warning("SecretId or SecretKey is None, attempting to use environment values.")
            if not self._try_set_secret_from_env():
                raise AuthenticationError("SecretId or SecretKey is not set")

        cred = Credential(self.config.SecretId, self.config.SecretKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = self.config.EndPoint
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile

        logger.info(
            f"Creating a new client for module: {self.config.Module}, version: {self.config.Version}, region: {self.config.Region}"
        )
        return CommonClient(
            self.config.Module,
            self.config.Version,
            cred,
            self.config.Region,
            profile=clientProfile,
        )

    def call(self, action: str, action_params: dict = {}, headers: dict = {}) -> Any:
        try:
            client = self.new_client()
            logger.info(f"Calling action: {action} with params: {action_params}")
            resp = client.call_json(action, action_params, headers=headers)
            return resp
        except AuthenticationError as err:
            logger.error(f"Authentication Error: {err}")
            raise err
        except ClientError as err:
            logger.error(f"Client Error: {err}")
            raise err
        except TencentCloudSDKException as err:
            raise err

    def call_with_retry(
        self, action: str, action_params: dict, max_retries: int = 5, retries: int = 0, retry_time: int = 5
    ) -> Any:
        """Calls Tencent Cloud API, retries if encountering errors related to ongoing tasks."""

        try:
            return self.call(action=action, action_params=action_params)
        except TencentCloudSDKException as err:
            if "tasks are being processed" in str(err) or "task is working" in str(err):
                if retries < max_retries:
                    retries += 1
                    logger.info(f"Task is being processed, retrying {retries}/{max_retries}")
                    sleep(retry_time)
                    return self.call_with_retry(action, action_params, max_retries, retries, retry_time)
                else:
                    logger.error("Maximum number of retries reached.")
                    raise err
            else:
                raise err
        except Exception as err:
            return err
