# -*- coding: utf-8 -*-

import json
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional

from .logging import logger
from .base import QcloudBase
from .exceptions import ServiceConfigError


class Services(QcloudBase):
    def __init__(
        self,
        name: str,
        region: str,
        secret_id: Optional[str] = None,
        secret_key: Optional[str] = None,
        version: Optional[str] = None,
    ):
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
        if data is None:
            logger.error(f"Service '{self._n}' not found")
            raise ServiceConfigError(f"Service '{self._n}' not found")
        if data.get("api_versions") is None:
            logger.error(f"Service '{self._n}' apiVersion is None")
            raise ServiceConfigError(f"Service '{self._n}' apiVersion is None")
        if data.get("endpoint") is None:
            logger.error(f"Service '{self._n}' endpoint is None")
            raise ServiceConfigError(f"Service '{self._n}' endpoint is None")
        if data.get("service") is None:
            logger.error(f"Service '{self._n}' service is None")
            raise ServiceConfigError(f"Service '{self._n}' service is None")

        # Check if the given version is available.
        if self._v is not None and self._v not in data.get("api_versions"):
            logger.error(f"Service '{self._n}' has no such api-version as '{self._v}'")
            raise ServiceConfigError(
                f"Service '{self._n}' has no such api-version as '{self._v}', ava versions {data.get('api_versions')}"
            )

    @staticmethod
    @lru_cache(maxsize=None)
    def _load_api_info() -> Dict[str, Dict]:
        data_dir = Path(__file__).parent / "data"
        json_files = list(data_dir.glob("endpoints_*.json"))
        if not json_files:
            logger.error("No api_info JSON files found")
            raise FileNotFoundError("No api_info JSON files found")
        filename = max(json_files)

        with open(filename, "r") as f:
            logger.info(f"Loading API info from {filename}")
            return json.load(f)

    @property
    def version(self) -> str:
        return self._v or max(self._d_vs)

    @property
    def endpoint(self) -> str:
        return self._d_e

    @property
    def name(self) -> str:
        return self._d_s

    @property
    def ava_versions(self) -> List[str]:
        return self._d_vs
