# pyqcloud-sdk

**English** · [简体中文](./README.zh-CN.md)

[![Python Versions](https://img.shields.io/pypi/pyversions/pyqcloud-sdk.svg)](https://pypi.org/project/pyqcloud-sdk)
[![PyPI version](https://badge.fury.io/py/pyqcloud-sdk.svg)](https://badge.fury.io/py/pyqcloud-sdk)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

pyqcloud-sdk is a Python package that simplifies the calling of Tencent Cloud product APIs. With just a product ID, region, operation code, and request parameters, you can achieve API calls. The main features are:

- Simplified and unified API calling method
- Automatic handling of authentication, region, and client settings
- Supports all services supported by the original SDK
- Supports custom log configuration
- Based on tencentcloud-sdk-python-common, providing a higher-level abstraction
- Pre-fetches product interface information from [tencentcloud-sdk-python](https://github.com/TencentCloud/tencentcloud-sdk-python/tree/master/tencentcloud)

## Installation

Install using pip:

```console
pip install pyqcloud-sdk
```

Supports Python 3.6+

## Quick Start

```python
import logging
from pyqcloud_sdk import Services, setup_logging

# Set up logging (optional)
setup_logging(level=logging.INFO)

# Initialize service
service = Services(
    name="cvm",                   # Service name, required
    region="ap-guangzhou",        # Region, required
  secret_id="your_secret_id",     # Optional, default reads from environment variable
    secret_key="your_secret_key", # Optional, default reads from environment variable
    version="2017-03-12"          # Optional, API version, default is the latest version
)

# Call API
response = service.call("DescribeInstances", {"Limit": 1})
print(response)
```

## Authentication Configuration

It is recommended to set authentication information using environment variables:

- Default reads `TENCENTCLOUD_SECRET_ID` and `TENCENTCLOUD_SECRET_KEY`
- Use `set_secret_from_env()` to specify custom environment variable names:

```python
service.set_secret_from_env('CUSTOM_ID_ENV', 'CUSTOM_KEY_ENV')
```

## Error Handling

```python
from pyqcloud_sdk.exceptions import ServiceError, ClientError

try:
    response = service.call("DescribeInstances", {})
except ServiceError as e:
    print(f"Service error: {e}")
except ClientError as e:
    print(f"Client error: {e}")
...
```

## Custom Logging

```python
from pyqcloud_sdk import setup_logging
import logging

setup_logging(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
```

## Notes

1. Keep SecretId and SecretKey safe and avoid leakage.
2. In production environments, it is recommended to store sensitive information using environment variables or configuration files.
3. This package automatically handles most API call retries, but special cases may require custom retry logic.
4. Before using, ensure that the necessary access permissions have been granted in the Tencent Cloud console and that the corresponding services have been enabled.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Related Links

- [Tencent Cloud API Documentation](https://cloud.tencent.com/document/api)
- [tencentcloud-sdk-python](https://github.com/TencentCloud/tencentcloud-sdk-python)
