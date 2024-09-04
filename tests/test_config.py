import unittest
from unittest.mock import patch

from pyqcloud_sdk.config import Config  # Adjust the import path as needed
from pyqcloud_sdk.logging import logger


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.config = Config()

    def test_init(self):
        """Test the initialization of Config object."""
        self.assertIsNone(self.config.Module)
        self.assertIsNone(self.config.Version)
        self.assertIsNone(self.config.EndPoint)
        self.assertIsNone(self.config.Region)
        self.assertIsNone(self.config.SecretId)
        self.assertIsNone(self.config.SecretKey)

    def test_deserialize_all_fields(self):
        """Test deserialization with all fields present."""
        config_dict = {
            "Module": "TestModule",
            "Version": "1.0",
            "EndPoint": "test.endpoint.com",
            "Region": "test-region",
            "SecretId": "test-secret-id",
            "SecretKey": "test-secret-key",
        }
        self.config._deserialize(config_dict)

        self.assertEqual(self.config.Module, "TestModule")
        self.assertEqual(self.config.Version, "1.0")
        self.assertEqual(self.config.EndPoint, "test.endpoint.com")
        self.assertEqual(self.config.Region, "test-region")
        self.assertEqual(self.config.SecretId, "test-secret-id")
        self.assertEqual(self.config.SecretKey, "test-secret-key")

    def test_deserialize_partial_fields(self):
        """Test deserialization with only some fields present."""
        config_dict = {
            "Module": "TestModule",
            "Version": "1.0",
        }
        self.config._deserialize(config_dict)

        self.assertEqual(self.config.Module, "TestModule")
        self.assertEqual(self.config.Version, "1.0")
        self.assertIsNone(self.config.EndPoint)
        self.assertIsNone(self.config.Region)
        self.assertIsNone(self.config.SecretId)
        self.assertIsNone(self.config.SecretKey)

    def test_deserialize_extra_fields(self):
        """Test deserialization with extra fields."""
        config_dict = {"Module": "TestModule", "ExtraField1": "extra1", "ExtraField2": "extra2"}

        with patch("pyqcloud_sdk.config.logger") as mock_logger:
            self.config._deserialize(config_dict)
            mock_logger.warning.assert_called_once_with("ExtraField1,ExtraField2 fields are useless.")

        self.assertEqual(self.config.Module, "TestModule")

    def test_deserialize_empty_dict(self):
        """Test deserialization with an empty dictionary."""
        self.config._deserialize({})

        self.assertIsNone(self.config.Module)
        self.assertIsNone(self.config.Version)
        self.assertIsNone(self.config.EndPoint)
        self.assertIsNone(self.config.Region)
        self.assertIsNone(self.config.SecretId)
        self.assertIsNone(self.config.SecretKey)


if __name__ == "__main__":
    unittest.main()
