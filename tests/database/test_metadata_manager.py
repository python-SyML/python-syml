import json
import unittest
import unittest.mock
from pathlib import Path
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from syml.database.metadata_manager import JSONFileHandler


class TestJSONFileHandler(unittest.TestCase):
    @patch("pathlib.Path.open", new_callable=MagicMock)
    def test_create_json_file_with_dictionary(self, mock_open):
        file_path = Path("../python-syml/config/config_test.json")
        json_file_handler = JSONFileHandler(file_path)
        data = {"key1": "value1", "key2": "value2"}

        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file

        json_file_handler.create_json_file(data)
        mock_open.assert_called_once_with("w")
        expected_calls = [
            unittest.mock.call(part)
            for part in ["{", "\n    ", '"key1"', ": ", '"value1"', ",\n    ", '"key2"', ": ", '"value2"', "\n", "}"]
        ]
        mock_file.write.assert_has_calls(expected_calls)

    @patch("pathlib.Path.open", new_callable=MagicMock)
    def test_create_json_file_with_list(self, mock_open):
        file_path = Path("../python-syml/config/config_test.json")
        json_file_handler = JSONFileHandler(file_path)
        data = ["item1", "item2", "item3"]

        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file

        json_file_handler.create_json_file(data)
        mock_open.assert_called_once_with("w")
        mock_file.write.assert_has_calls(
            [
                unittest.mock.call('[\n    "item1"'),
                unittest.mock.call(',\n    "item2"'),
                unittest.mock.call(',\n    "item3"'),
                unittest.mock.call("\n"),
                unittest.mock.call("]"),
            ]
        )

    @patch("pathlib.Path.open", new_callable=MagicMock)
    def test_create_json_file_with_nested_dict_and_list(self, mock_open):
        file_path = Path("../python-syml/config/config_test.json")
        json_file_handler = JSONFileHandler(file_path)
        data = {
            "key1": "value1",
            "key2": ["item1", "item2", "item3"],
            "key3": {"sub_key1": "sub_value1", "sub_key2": ["sub_item1", "sub_item2"]},
        }
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file

        json_file_handler.create_json_file(data)
        mock_open.assert_called_once_with("w")
        mock_file.write.assert_has_calls(
            [
                unittest.mock.call("{"),
                unittest.mock.call("\n    "),
                unittest.mock.call('"key1"'),
                unittest.mock.call(": "),
                unittest.mock.call('"value1"'),
                unittest.mock.call(",\n    "),
                unittest.mock.call('"key2"'),
                unittest.mock.call(": "),
                unittest.mock.call('[\n        "item1"'),
                unittest.mock.call(',\n        "item2"'),
                unittest.mock.call(',\n        "item3"'),
                unittest.mock.call("\n    "),
                unittest.mock.call("]"),
                unittest.mock.call(",\n    "),
                unittest.mock.call('"key3"'),
                unittest.mock.call(": "),
                unittest.mock.call("{"),
                unittest.mock.call("\n        "),
                unittest.mock.call('"sub_key1"'),
                unittest.mock.call(": "),
                unittest.mock.call('"sub_value1"'),
                unittest.mock.call(",\n        "),
                unittest.mock.call('"sub_key2"'),
                unittest.mock.call(": "),
                unittest.mock.call('[\n            "sub_item1"'),
                unittest.mock.call(',\n            "sub_item2"'),
                unittest.mock.call("\n        "),
                unittest.mock.call("]"),
                unittest.mock.call("\n    "),
                unittest.mock.call("}"),
                unittest.mock.call("\n"),
                unittest.mock.call("}"),
            ]
        )

    @patch("pathlib.Path.open", new_callable=MagicMock)
    def test_create_json_file_with_empty_dictionary(self, mock_open):
        file_path = Path("../python-syml/config/config_test.json")
        json_file_handler = JSONFileHandler(file_path)
        data = {}

        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file

        json_file_handler.create_json_file(data)
        mock_open.assert_called_once_with("w")
        mock_file.write.assert_called_once_with(json.dumps(data, indent=4))

    @patch("pathlib.Path.open", new_callable=MagicMock)
    def test_create_json_file_with_empty_list(self, mock_open):
        file_path = Path("../python-syml/config/config_test.json")
        json_file_handler = JSONFileHandler(file_path)
        data = []

        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file

        json_file_handler.create_json_file(data)
        mock_open.assert_called_once_with("w")
        mock_file.write.assert_called_once_with(json.dumps(data, indent=4))

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

    def test_read_json_file_with_non_existing_file(self):
        file_path = Path("../python-syml/config/non_existing_file.json")
        json_file_handler = JSONFileHandler(file_path)

        result = json_file_handler.read_json_file()
        assert result is None

    def test_read_json_file_invalid_json_format(self):
        invalid_file_path = Path("../python-syml/config/invalid_json_format.json")
        json_file_handler = JSONFileHandler(invalid_file_path)

        result = json_file_handler.read_json_file()

        assert result is None

    def test_read_json_file_with_empty_dictionary(self):
        file_path = Path("../python-syml/config/config_test.json")
        json_file_handler = JSONFileHandler(file_path)

        json_file_handler.create_json_file({})
        with pytest.warns(UserWarning, match="JSON file is empty."):
            result = json_file_handler.read_json_file()

        assert result is None

    def test_read_json_file_with_empty_list(self):
        file_path = Path("../python-syml/config/config_test.json")
        json_file_handler = JSONFileHandler(file_path)

        json_file_handler.create_json_file([])
        with pytest.warns(UserWarning, match="JSON file is empty."):
            result = json_file_handler.read_json_file()

        assert result is None
