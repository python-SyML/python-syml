import json
import unittest
from pathlib import Path
from unittest.mock import Mock
from unittest.mock import patch

import pytest

from syml.database.metadata_manager import JSONFileHandler


class TestJSONFileHandler(unittest.TestCase):
    def test_create_json_file_with_dictionary(self):
        file_path = Path("../python-syml/config/config_test.json")
        json_file_handler = JSONFileHandler(file_path)
        data = {"key1": "value1", "key2": "value2"}

        with patch("builtins.open", new_callable=Mock) as mock_open:
            json_file_handler.create_json_file(data)
            mock_open.assert_called_once_with(file_path, "w")
            mock_open().write.assert_called_once_with(json.dumps(data, indent=4))

    def test_create_json_file_with_list(self):
        file_path = Path("../python-syml/config/config_test.json")
        json_file_handler = JSONFileHandler(file_path)
        data = ["item1", "item2", "item3"]

        with patch("builtins.open", new_callable=Mock) as mock_open:
            json_file_handler.create_json_file(data)
            mock_open.assert_called_once_with(file_path, "w")
            mock_open().write.assert_called_once_with(json.dumps(data, indent=4))

    def test_create_json_file_with_nested_dict_and_list(self):
        file_path = Path("../python-syml/config/config_test.json")
        json_file_handler = JSONFileHandler(file_path)
        data = {
            "key1": "value1",
            "key2": ["item1", "item2", "item3"],
            "key3": {"sub_key1": "sub_value1", "sub_key2": ["sub_item1", "sub_item2"]},
        }

        with patch("builtins.open", new_callable=Mock) as mock_open:
            json_file_handler.create_json_file(data)
            mock_open.assert_called_once_with(file_path, "w")
            mock_open().write.assert_called_once_with(json.dumps(data, indent=4))

    def test_create_json_file_with_empty_dictionary(self):
        file_path = Path("../python-syml/config/config_test.json")
        json_file_handler = JSONFileHandler(file_path)
        data = {}

        with patch("builtins.open", new_callable=Mock) as mock_open:
            json_file_handler.create_json_file(data)
            mock_open.assert_called_once_with(file_path, "w")
            mock_open().write.assert_called_once_with(json.dumps(data, indent=4))

    def test_create_json_file_with_empty_list(self):
        file_path = Path("../python-syml/config/config_test.json")
        json_file_handler = JSONFileHandler(file_path)
        data = []

        with patch("builtins.open", new_callable=Mock) as mock_open:
            json_file_handler.create_json_file(data)
            mock_open.assert_called_once_with(file_path, "w")
            mock_open().write.assert_called_once_with(json.dumps(data, indent=4))

    def test_create_json_file_with_invalid_file_path(self):
        invalid_file_path = "/path/to/invalid/file.json"
        json_file_handler = JSONFileHandler(invalid_file_path)

        with pytest.raises(FileNotFoundError):
            json_file_handler.create_json_file({"key1": "value1"})

    def test_create_json_file_with_invalid_data_type(self):
        file_path = Path("../python-syml/config/config_test.json")
        json_file_handler = JSONFileHandler(file_path)
        invalid_data = "invalid_data"

        with pytest.raises(TypeError):
            json_file_handler.create_json_file(invalid_data)
