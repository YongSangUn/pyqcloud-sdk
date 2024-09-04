# -*- coding: utf-8 -*-


class ServiceError(Exception):
    pass


class ServiceJsonNotFoundError(ServiceError):
    pass


class ServiceJsonLoadError(ServiceError):
    pass


class ClientError(Exception):
    pass


class ConfigError(ClientError):
    pass


class AuthenticationError(ConfigError):
    pass
