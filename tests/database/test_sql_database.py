import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock
from unittest.mock import patch

import pandas as pd

from syml.database.sql_database import SQLDatabase


class TestInitTables(unittest.TestCase):
    def setUp(self):
        # Specify the directory where the temporary folder should be created
        self.base_temp_dir_config = "../python-syml/tests"
        # Create a temporary directory at the specified path
        self.temp_dir_config = tempfile.mkdtemp(dir=self.base_temp_dir_config)
        self.base_temp_dir_data = "../python-syml/tests"
        # Create a temporary directory at the specified path
        self.temp_dir_data = tempfile.mkdtemp(dir=self.base_temp_dir_data)

        self.sql_db = SQLDatabase(db_path=f"{self.temp_dir_data}/database_test.db", metadata_path=f"{self.temp_dir_config}/metadata.json")
        self.original_cwd = Path.cwd()

    def tearDown(self):
        # Clean up the temporary directory
        self.sql_db.close_connection()
        shutil.rmtree(self.temp_dir_data)
        shutil.rmtree(self.temp_dir_config)
        os.chdir(self.original_cwd)

    def test_init_tables_returns_empty_dict(self):
        with patch.object(self.sql_db, "metadata_manager", new_callable=MagicMock) as mock_object:
            mock_object.read_json_file.return_value = None
            result = self.sql_db.init_tables()
            assert result == {}
            mock_object.read_json_file.assert_called_once()

    @patch("syml.database.sql_database.JSONFileHandler.read_json_file")
    def test_init_tables_returns_same_dictionary(self, mock_read_json_file):
        mock_read_json_file.return_value = {"table1": {"columns": ["col1", "col2"]}, "table2": {"columns": ["col3", "col4"]}}
        result = self.sql_db.init_tables()
        assert result == {"table1": {"columns": ["col1", "col2"]}, "table2": {"columns": ["col3", "col4"]}}

    def test_create_table_from_dataframe_single_column(self):
        df = pd.DataFrame({"col1": [1, 2, 3]})
        table_name = "test_table"
        self.sql_db.generate_database(table_name=table_name, df=df)
        res = self.sql_db.query(f"SELECT * FROM {table_name}")  # noqa: S608
        pd.testing.assert_frame_equal(res, df)

    def test_create_table_from_dataframe_with_mixed_data_types(self):
        df = pd.DataFrame({"A": [1, 2, 3], "B": [1.1, 2.2, 3.3], "C": ["a", "b", "c"]})
        table_name = "test_table"
        self.sql_db.generate_database(table_name=table_name, df=df)
        res = self.sql_db.query(f"SELECT * FROM {table_name}")  # noqa: S608
        pd.testing.assert_frame_equal(res, df)

    def test_query_returns_empty_dataframe(self):
        result = self.sql_db.query("SELECT * FROM non_existing_table")

        assert len(result) == 0

    def test_query_with_limit_and_offset(self):
        df = pd.DataFrame([[1, "a"], [2, "b"], [3, "c"]], columns=["id", "name"])

        self.sql_db.generate_database(df=df, table_name="test_table")

        result = self.sql_db.query("SELECT * FROM test_table LIMIT 2 OFFSET 1")

        assert len(result) == 2
        assert result.iloc[0]["id"] == 2
        assert result.iloc[0]["name"] == "b"
        assert result.iloc[1]["id"] == 3
        assert result.iloc[1]["name"] == "c"
