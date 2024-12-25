import sqlite3

import pandas as pd

from .utils import reformat_string


class SQLDatabase:
    def __init__(self, db_path="../data/database.db"):
        self.db_path = db_path
        self.tables = {}
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()

    def read_csv(self, csv_file):
        self.df = pd.read_csv(csv_file).drop(columns=["Unnamed: 0"])

    def create_table_from_dataframe(self, table_name, df):
        self.tables[table_name] = {}
        col_type = ", ".join([f"{reformat_string(col)} {self._map_dtype(df[col].dtype)}" for col in df.columns])
        self.tables[table_name]["sql_columns"] = [reformat_string(col) for col in df.columns]
        self.tables[table_name]["n_columns"] = len(df.columns)
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({col_type})"
        self.cursor.execute(create_table_query)
        self.connection.commit()

    def insert_data_from_dataframe(self, table_name, df):
        placeholder = ["?"] * self.tables[table_name]["n_columns"]
        insert_query = f"INSERT INTO {table_name} VALUES({', '.join(placeholder)})"
        data_tuple = [tuple(row) for row in df.itertuples(index=False, name=None)]
        self.cursor.executemany(insert_query, data_tuple)
        self.connection.commit()

    def _map_dtype(self, dtype):
        if pd.api.types.is_integer_dtype(dtype):
            return "INTEGER"
        elif pd.api.types.is_float_dtype(dtype):
            return "REAL"
        else:
            return "TEXT"

    def generate_database(self, csv_file="", table_name="dataset"):
        self.read_csv(csv_file)
        self.create_table_from_dataframe(table_name, self.df)
        self.insert_data_from_dataframe(table_name, self.df)

    def close_connection(self):
        self.connection.close()