import logging

from pyqcloud_sdk import Services

logging.basicConfig(level=logging.INFO)


try:
    cvm = Services("cvm", "ap-shanghai")
    action = "DescribeInstances"
    params = {"Limit": 1}
    res = cvm.call(action, params)
    print(res)
    # Use retries to avoid errors caused by a large number of operations within
    # a short time frame, which can occur during console operations.
    res_r = cvm.call_with_retry(action, params)
    print(res_r)
except Exception as e:
    print(e)
