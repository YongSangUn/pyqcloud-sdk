# -*- coding: utf-8 -*-

import json
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional

from .logging import logger
from .base import QcloudBase
from .exceptions import (
    ServiceDefinitionError,
    ServiceDiscoveryError,
    ServiceNotFoundError,
)


class Services(QcloudBase):
    """Represents a collection of available Tencent Cloud services."""

    def __init__(
        self,
        name: str,
        region: str,
        secret_id: Optional[str] = None,
        secret_key: Optional[str] = None,
        version: Optional[str] = None,
    ):
        """
        Initializes a Services object.

        Args:
            name (str): The name of the Tencent Cloud service.
            region (str): The region where the service is located.
            secret_id (Optional[str], optional): The Tencent Cloud SecretId. Defaults to None.
            secret_key (Optional[str], optional): The Tencent Cloud SecretKey. Defaults to None.
            version (Optional[str], optional): The API version of the service. Defaults to None.

        Raises:
            ServiceDiscoveryError: If there's an error during service discovery.
        """
        self._v = version
        self._n = name
        _info = self._load_api_info()
        _d = _info.get(name)
        self._check(_d)
        self._d_vs = _d["api_versions"]
        self._d_e = _d["endpoint"]
        self._d_s = _d["service"]

        super().__init__(
            {
                "Module": self.name,
                "Version": self.version,
                "EndPoint": self.endpoint,
                "Region": region,
                "SecretId": secret_id,
                "SecretKey": secret_key,
            },
        )
        logger.info(f"Service initialized: {self._n} in region: {region}")

    def _check(self, data):
        """
        Validates the loaded service information.

        Args:
            data (dict): The loaded service information.

        Raises:
            ServiceNotFoundError: If the service is not found.
            ServiceDefinitionError: If the service definition is invalid.
        """
        if data is None:
            raise ServiceNotFoundError(f"Service '{self._n}' not found")
        for key, msg in [
            ("api_versions", "apiVersion"),
            ("endpoint", "endpoint"),
            ("service", "service"),
        ]:
            if data.get(key) is None:
                raise ServiceDefinitionError(f"Service '{self._n}' {msg} is None")

        # Check if the given version is available.
        if self._v is not None and self._v not in data.get("api_versions"):
            raise ServiceDefinitionError(
                f"Service '{self._n}' has no such api-version as '{self._v}', "
                f"available versions: {data.get('api_versions')}"
            )

    @staticmethod
    @lru_cache(maxsize=None)
    def _load_api_info() -> Dict[str, Dict]:
        """
        Loads API information from local JSON files.

        Returns:
            Dict[str, Dict]: A dictionary containing API information for each service.

        Raises:
            ServiceDiscoveryError: If no API info JSON files are found or if there's an error loading them.
        """
        data_dir = Path(__file__).parent / "data"
        json_files = list(data_dir.glob("endpoints_*.json"))
        if not json_files:
            raise ServiceDiscoveryError("No api_info JSON files found")
        filename = max(json_files)

        with open(filename, "r") as f:
            logger.info(f"Loading API info from {filename}")
            try:
                return json.load(f)
            except Exception as err:
                raise ServiceDiscoveryError(f"Loading error: {err}") from err

    @property
    def version(self) -> str:
        """str: The API version of the service."""
        return self._v or max(self._d_vs)

    @property
    def endpoint(self) -> str:
        """str: The endpoint URL of the service."""
        return self._d_e

    @property
    def name(self) -> str:
        """str: The name of the service."""
        return self._d_s

    @property
    def ava_versions(self) -> List[str]:
        """List[str]: A list of available API versions for the service."""
        return self._d_vs
