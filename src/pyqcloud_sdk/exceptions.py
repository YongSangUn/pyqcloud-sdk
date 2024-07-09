# -*- coding: utf-8 -*-


class TencentCloudAPIError(Exception):
    """Base exception for Tencent Cloud API errors"""

    pass


class ServiceConfigError(TencentCloudAPIError):
    """Raised when a requested service is not found"""

    pass


class QcloudExceptrion(Exception):
    """Qcloud Exception class"""

    def __init__(self, code: str = None, message: str = None) -> None:
        self.code = code
        self.message = message

    def __str__(self) -> str:
        return f"[QcloudExceptrion] code:{self.code} message:{self.message}"

    def get_code(self) -> str:
        return self.code

    def get_message(self) -> str:
        return self.message
