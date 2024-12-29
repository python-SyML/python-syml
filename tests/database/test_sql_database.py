import unittest
from unittest.mock import MagicMock
from unittest.mock import patch

import pandas as pd

from syml.database.sql_database import SQLDatabase


class TestInitTables(unittest.TestCase):
    def setUp(self):
        self.sql_db = SQLDatabase(db_path="../python-syml/data/database.db", metadata_path="../python-syml/config/metadata.json")

    def test_init_tables_returns_empty_dict(self):
        with patch.object(self.sql_db, "metadata_manager", new_callable=MagicMock) as mock_object:
            mock_object.read_json_file.return_value = None
            result = self.sql_db.init_tables()
            assert result == {}
            mock_object.read_json_file.assert_called_once()

    @patch("syml.database.sql_database.JSONFileHandler.read_json_file")
    def test_init_tables_returns_same_dictionary(self, mock_read_json_file):
        mock_read_json_file.return_value = {"table1": {"columns": ["col1", "col2"]}, "table2": {"columns": ["col3", "col4"]}}
        sql_db = SQLDatabase(db_path="../python-syml/data/database.db", metadata_path="../python-syml/config/metadata.json")
        result = sql_db.init_tables()
        assert result == {"table1": {"columns": ["col1", "col2"]}, "table2": {"columns": ["col3", "col4"]}}


class TestCreateTableFromDataframe(unittest.TestCase):
    def test_create_table_from_dataframe_single_column(self):
        sql_db = SQLDatabase(db_path="../python-syml/data/database_test.db", metadata_path="../python-syml/config/metadata_test.json")
        df = pd.DataFrame({"col1": [1, 2, 3]})
        table_name = "test_table"
        sql_db.generate_database(table_name=table_name, df=df)
        res = sql_db.query(f"SELECT * FROM {table_name}")  # noqa: S608
        pd.testing.assert_frame_equal(res, df)

    def test_create_table_from_dataframe_with_mixed_data_types(self):
        sql_db = SQLDatabase(db_path="../python-syml/data/database_test.db", metadata_path="../python-syml/config/metadata_test.json")
        df = pd.DataFrame({"A": [1, 2, 3], "B": [1.1, 2.2, 3.3], "C": ["a", "b", "c"]})
        table_name = "test_table"
        sql_db.generate_database(table_name=table_name, df=df)
        res = sql_db.query(f"SELECT * FROM {table_name}")  # noqa: S608
        pd.testing.assert_frame_equal(res, df)


class TestQueryReturnsEmptyDataFrame(unittest.TestCase):
    @patch("syml.database.sql_database.SQLDatabase.query")
    def test_query_returns_empty_dataframe(self, mock_query):
        mock_query.return_value = pd.DataFrame()
        sql_db = SQLDatabase(db_path="../python-syml/data/database_test.db", metadata_path="../python-syml/config/metadata_test.json")
        result = sql_db.query("SELECT * FROM non_existing_table")
        mock_query.assert_called_once_with("SELECT * FROM non_existing_table")
        assert len(result) == 0

    @patch("syml.database.sql_database.SQLDatabase.query")
    def test_query_with_order_by_and_group_by(self, mock_query):
        mock_query.return_value = pd.DataFrame()
        sql_db = SQLDatabase(db_path="../python-syml/data/database_test.db", metadata_path="../python-syml/config/metadata_test.json")
        query = "SELECT * FROM test_table GROUP BY col1 ORDER BY col2 DESC"
        _ = sql_db.query(query)
        mock_query.assert_called_once_with(query)

    def test_query_with_limit_and_offset(self):
        df = pd.DataFrame([[1, "a"], [2, "b"], [3, "c"]], columns=["id", "name"])

        sql_db = SQLDatabase(db_path="../python-syml/data/database_test.db", metadata_path="../python-syml/config/metadata_test.json")

        sql_db.generate_database(df=df, table_name="test_table")

        result = sql_db.query("SELECT * FROM test_table LIMIT 2 OFFSET 1")

        assert len(result) == 2
        assert result.iloc[0]["id"] == 2
        assert result.iloc[0]["name"] == "b"
        assert result.iloc[1]["id"] == 3
        assert result.iloc[1]["name"] == "c"
