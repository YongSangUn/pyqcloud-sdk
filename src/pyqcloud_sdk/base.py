# -*- coding: utf-8 -*-


import os
from time import sleep
from typing import Tuple, Union

from tencentcloud.common.common_client import CommonClient
from tencentcloud.common.credential import Credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile

from .logging import logger
from .exceptions import QcloudExceptrion
from .config import Config


class QcloudBase:
    def __init__(self, service_config: dict):
        self.config = Config()
        self.config._deserialize(service_config)
        if not self.config.Region:
            raise QcloudExceptrion("RegionError", "Parameter 'region' is None")
        logger.info(f"QcloudBase initialized with region: {self.config.Region}")

    def set_region(self, region: str):
        self.config.Region = region
        logger.info(f"Region set to: {region}")

    def set_secret_key(self, secretKey: str):
        self.config.SecretKey = secretKey
        logger.info("SecretKey set.")

    def set_secret_id(self, secretId: str):
        self.config.SecretId = secretId
        logger.info("SecretId set.")

    def set_secret_from_env(
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
            if not self.set_secret_from_env():
                raise QcloudExceptrion("SecretParamsError", "SecretId or SecretKey is not set")

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

    def call(
        self, action: str, action_params: dict, headers: dict = {}
    ) -> Union[Tuple[None, dict], Tuple[str, Exception]]:
        try:
            client = self.new_client()
            logger.info(f"Calling action: {action} with params: {action_params}")
            resp = client.call_json(action, action_params, headers=headers)
            return None, resp
        except QcloudExceptrion as err:
            logger.error(f"QcloudExceptrion: {err}")
            return err.code, err
        except TencentCloudSDKException as err:
            logger.error(f"TencentCloudSDKException: {err}")
            return err.code, err  # type: ignore

    def call_with_retry(
        self, action: str, action_params: dict, max_retries: int = 5, retries: int = 0, retry_time: int = 5
    ) -> Tuple[Union[None, str], Union[dict, Exception]]:
        err, resp = self.call(action=action, action_params=action_params)
        if err:
            err_msg = str(resp)
            if "tasks are being processed" in err_msg or "task is working" in err_msg:
                if retries < max_retries:
                    logger.info(f"Task is being processed, retrying {retries + 1}/{max_retries}")
                    sleep(retry_time)
                    return self.call_with_retry(action, action_params, max_retries, retries + 1, retry_time)
                else:
                    logger.error("Maximum number of retries reached.")
                    return err, resp
        return err, resp
