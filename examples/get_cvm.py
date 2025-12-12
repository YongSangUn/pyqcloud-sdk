import logging
import os

from pyqcloud_sdk import Services

logging.basicConfig(level=logging.INFO)


def example_with_default_env():
    """Example using default environment variable names."""
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


def example_with_custom_env():
    """Example using custom environment variable names."""
    # Set custom environment variables for demonstration
    os.environ['MY_CUSTOM_SECRET_ID'] = 'your_secret_id_here'
    os.environ['MY_CUSTOM_SECRET_KEY'] = 'your_secret_key_here'

    try:
        # Use custom environment variable names
        cvm = Services(
            "cvm",
            "ap-shanghai",
            secret_id_env_name='MY_CUSTOM_SECRET_ID',
            secret_key_env_name='MY_CUSTOM_SECRET_KEY'
        )
        action = "DescribeInstances"
        params = {"Limit": 1}
        res = cvm.call(action, params)
        print("Custom env example result:", res)
    except Exception as e:
        print("Custom env example error:", e)
    finally:
        # Clean up custom environment variables
        if 'MY_CUSTOM_SECRET_ID' in os.environ:
            del os.environ['MY_CUSTOM_SECRET_ID']
        if 'MY_CUSTOM_SECRET_KEY' in os.environ:
            del os.environ['MY_CUSTOM_SECRET_KEY']


if __name__ == "__main__":
    print("=== Default Environment Variables Example ===")
    example_with_default_env()

    print("\n=== Custom Environment Variables Example ===")
    example_with_custom_env()
