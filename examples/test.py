import logging

from pyqcloud_sdk import Services

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


cvm = Services("cvm", "ap-shanghai")

action = "DescribeInstances"
params = {"Limit": 1}
print(cvm.call_with_retry(action, params))
