# PyQCloud SDK

PyQCloud SDK 是一个用于简化调用腾讯云 API 的 Python 库。通过使用 `tencentcloud-sdk-python-common` 包和预先爬取的 `endpoints_*.json` 数据文件，该 SDK 提供了便捷的方式来与腾讯云的各种服务进行交互。

## 使用

以下是一个简单的使用示例：

```python
from pyqcloud_sdk import Services

cvm = Services("cvm", "ap-shanghai")
action = "DescribeInstances"
params = {"Limit": 1}
err, res = cvm.call(action, params) # 或者 cvm.call_wite_retry(action, params)
print(err, res)
```

## 许可证

该项目基于 MIT 许可证开源。详情请参阅 LICENSE 文件。
