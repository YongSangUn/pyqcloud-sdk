# pyqcloud-sdk

[English](./README.md) · **简体中文**

[![Python Versions](https://img.shields.io/pypi/pyversions/pyqcloud-sdk.svg)](https://pypi.org/project/pyqcloud-sdk)
[![PyPI version](https://badge.fury.io/py/pyqcloud-sdk.svg)](https://badge.fury.io/py/pyqcloud-sdk)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

pyqcloud-sdk 是一个简化腾讯云产品 API 调用的 Python 包。只需使用产品 ID、地域、执行操作代码及请求参数即可实现调用，主要特性：

- 简化及统一 API 调用方式
- 自动处理认证、区域等客户端设置
- 支持所有原 SDK 中支持的服务
- 支持自定义日志配置
- 基于 tencentcloud-sdk-python-common 提供更高层次的抽象
- 预先爬取 [tencentcloud-sdk-python](https://github.com/TencentCloud/tencentcloud-sdk-python/tree/master/tencentcloud) 中的产品接口信息

## 安装

使用 pip 安装：

```console
pip install pyqcloud-sdk
```

支持 Python 3.6+

## 快速开始

```python
import logging
from pyqcloud_sdk import Services, setup_logging

# 设置日志（可选）
setup_logging(level=logging.INFO)

# 初始化服务
service = Services(
    name="cvm",                   # 服务名称，必填
    region="ap-guangzhou",        # 区域，必填
    secret_id="your_secret_id",   # 可选，默认读取环境变量
    secret_key="your_secret_key", # 可选，默认读取环境变量
    version="2017-03-12"          # 可选，API 版本，默认为最新版本
)

# 调用 API
response = service.call("DescribeInstances", {"Limit": 1})
print(response)
```

## 认证配置

推荐使用环境变量设置认证信息：

- 默认读取 `TENCENTCLOUD_SECRET_ID` 和 `TENCENTCLOUD_SECRET_KEY`
- 使用 `set_secret_from_env()` 指定自定义环境变量名：

```python
service.set_secret_from_env('CUSTOM_ID_ENV', 'CUSTOM_KEY_ENV')
```

## 错误处理

```python
from pyqcloud_sdk.exceptions import ServiceError, ClientError

try:
    response = service.call("DescribeInstances", {})
except ServiceError as e:
    print(f"服务错误: {e}")
except ClientError as e:
    print(f"客户端错误: {e}")
...
```

## 自定义日志

```python
from pyqcloud_sdk import setup_logging
import logging

setup_logging(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
```

## 注意事项

1. 妥善保管 SecretId 和 SecretKey，避免泄露。
2. 生产环境建议使用环境变量或配置文件存储敏感信息。
3. 本包自动处理大多数 API 调用重试，特殊情况可能需要自定义重试逻辑。
4. 使用前确保已在腾讯云控制台开通相应服务并获取必要访问权限。

## 许可证

本项目采用 MIT 许可证。详情请参见 [LICENSE](LICENSE) 文件。

## 相关链接

- [腾讯云 API 文档](https://cloud.tencent.com/document/api)
- [tencentcloud-sdk-python](https://github.com/TencentCloud/tencentcloud-sdk-python)
