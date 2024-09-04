# -*- coding: utf-8 -*-

import os
from time import sleep
from typing import Any, Optional

from tencentcloud.common.common_client import CommonClient
from tencentcloud.common.credential import Credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile

from .config import Config
from .exceptions import (
    AuthenticationError,
    ClientError,
    QcloudWrapperError,
    ServerError,
)
from .logging import logger


class QcloudBase:
    """Base class for interacting with Tencent Cloud services."""

    def __init__(self, service_config: dict, client: Optional[CommonClient] = None):
        """
        Initializes a QcloudBase object.

        Args:
            service_config (dict): Configuration settings for the Tencent Cloud service.
            client (Optional[CommonClient], optional): An optional instance of CommonClient.
                                                       If not provided, one will be created.
        """
        self.config = Config()
        self.config._deserialize(service_config)
        self.client = client

    def set_region(self, region: str):
        """
        Sets the region for the Tencent Cloud client.

        Args:
            region (str): The region to use.
        """
        self.config.Region = region
        logger.info(f"Region set to: {region}")

    def set_secret_key(self, secret_key: str):
        """
        Sets the SecretKey for authentication.

        Args:
            secret_key (str): The Tencent Cloud SecretKey.
        """
        self.config.SecretKey = secret_key
        logger.info("SecretKey set.")

    def set_secret_id(self, secret_id: str):
        """
        Sets the SecretId for authentication.

        Args:
            secret_id (str): The Tencent Cloud SecretId.
        """
        self.config.SecretId = secret_id
        logger.info("SecretId set.")

    def _try_set_secret_from_env(
        self,
        id_env_name: str = "TENCENTCLOUD_SECRET_ID",
        key_env_name: str = "TENCENTCLOUD_SECRET_KEY",
    ) -> bool:
        """
        Attempts to set the SecretId and SecretKey from environment variables.

        Args:
            id_env_name (str, optional): The environment variable name for SecretId.
                                        Defaults to "TENCENTCLOUD_SECRET_ID".
            key_env_name (str, optional): The environment variable name for SecretKey.
                                        Defaults to "TENCENTCLOUD_SECRET_KEY".

        Returns:
            bool: True if successful, False otherwise.
        """
        secret_id = os.environ.get(id_env_name)
        secret_key = os.environ.get(key_env_name)
        if not secret_id or not secret_key:
            logger.warning("SecretId or SecretKey environment variable is not set.")
            return False

        self.config.SecretId, self.config.SecretKey = secret_id, secret_key
        logger.info("Secrets set from environment variables.")
        return True

    def _get_client(self) -> CommonClient:
        """
        Creates or returns an instance of CommonClient.

        Returns:
            CommonClient: An instance of CommonClient for making API calls.

        Raises:
            AuthenticationError: If authentication fails.
        """
        if self.client:
            return self.client

        if not self.config.SecretId or not self.config.SecretKey:
            logger.warning("SecretId or SecretKey is None, attempting to use environment values.")
            if not self._try_set_secret_from_env():
                raise AuthenticationError("SecretId or SecretKey is not set")

        cred = Credential(self.config.SecretId, self.config.SecretKey)
        http_profile = HttpProfile()
        http_profile.endpoint = self.config.EndPoint
        client_profile = ClientProfile()
        client_profile.httpProfile = http_profile

        logger.info(
            f"Creating a new client for module: {self.config.Module}, "
            f"version: {self.config.Version}, region: {self.config.Region}"
        )
        return CommonClient(
            self.config.Module,
            self.config.Version,
            cred,
            self.config.Region,
            profile=client_profile,
        )

    def call(self, action: str, action_params: dict = {}, headers: dict = {}) -> Any:
        """
        Makes a request to a Tencent Cloud API.

        Args:
            action (str): The API action to perform.
            action_params (dict, optional): Parameters for the API call. Defaults to {}.
            headers (dict, optional): Additional headers for the request. Defaults to {}.

        Returns:
            Any: The API response data.

        Raises:
            AuthenticationError: If authentication fails.
            ClientError: For other client-side errors.
            ServerError: For errors originating from the Tencent Cloud server.
        """
        try:
            client = self._get_client()
            logger.info(f"Calling action: {action} with params: {action_params}, headers: {headers}")
            resp = client.call_json(action, action_params, headers=headers)
            logger.debug(f"Response: {resp}")

            if isinstance(resp, dict) and resp.get("Response", {}).get("Error"):
                error_info = resp["Response"]["Error"]
                raise ServerError(
                    error_info.get("Message", "Tencent Cloud API Error"),
                    error_info.get("RequestId"),
                )

            return resp
        except AuthenticationError as err:
            logger.error(f"Authentication Error: {err}")
            raise err
        except ClientError as err:
            logger.error(f"Client Error: {err}")
            raise err
        except TencentCloudSDKException as err:
            logger.error(f"Tencent Cloud SDK Exception: {err}")
            raise ServerError(str(err)) from err
        except Exception as err:
            logger.exception(f"An unexpected error occurred: {err}")
            raise QcloudWrapperError(f"An unexpected error occurred: {err}") from err

    def call_with_retry(
        self,
        action: str,
        action_params: dict,
        max_retries: int = 5,
        retries: int = 0,
        retry_time: int = 5,
    ) -> Any:
        """
        Calls Tencent Cloud API, retries if encountering errors related to ongoing tasks.

        Args:
            action (str): The API action to perform.
            action_params (dict): Parameters for the API call.
            max_retries (int, optional): Maximum number of retries. Defaults to 5.
            retries (int, optional): Current retry count. Defaults to 0.
            retry_time (int, optional): Time to sleep between retries (in seconds). Defaults to 5.

        Returns:
            Any: The API response data.

        Raises:
            ServerError: If the maximum number of retries is reached and the error persists.
        """
        try:
            return self.call(action=action, action_params=action_params)
        except ServerError as err:
            if "tasks are being processed" in str(err) or "task is working" in str(err):
                if retries < max_retries:
                    retries += 1
                    logger.info(f"Task is being processed, retrying {retries}/{max_retries}")
                    sleep(retry_time)
                    return self.call_with_retry(action, action_params, max_retries, retries, retry_time)
                else:
                    logger.error("Maximum number of retries reached.")
                    raise
            else:
                raise
        except Exception as err:
            logger.exception(f"An unexpected error occurred: {err}")
            raise QcloudWrapperError(f"An unexpected error occurred: {err}") from err
