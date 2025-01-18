import json
import os
import re
from pathlib import Path

import pandas as pd


def reformat_string(s):
    return s.replace(":", "").replace("-", "_").replace(" ", "_")


def find_table_name(query):
    """
    Find the table name in a SQL query.

    :param query: SQL query string
    :return: Table name or None if not found
    """
    # Regular expression to match table names in simple SELECT, INSERT, UPDATE, DELETE queries
    pattern = r"\b(FROM|INTO|UPDATE|DELETE)\s+([a-zA-Z_][a-zA-Z0-9_]*)\b"
    match = re.search(pattern, query, re.IGNORECASE)

    if match:
        return match.group(2)
    else:
        return None


def read_config(selected_config: str, config_folder: str = "../config") -> dict:
    """
    Reads and merges JSON config files based on the selected configuration.

    The selected_config is expected to be a string in the format 'xxx_yyy_zzz',
    and the corresponding config files will be selected and merged according to the components
    of the input string, e.g., 'base', 'base_eu', 'base_eu_votes'.

    Args:
        selected_config (str): The name of the config file without the json extension (in the format 'xxx_yyy_zzz').
        config_folder (str): The folder containing the JSON config files. Defaults to "config".

    Returns:
        dict: A dictionary containing the merged content of the relevant config files.
    """

    # Split the base name into parts to determine which files to load
    config_parts = selected_config.split("_")

    # Initialize an empty dictionary to store the merged data
    merged_data = {}

    # Iterate through the parts and read the corresponding JSON files
    for i in range(1, len(config_parts) + 1):
        config_file = "_".join(config_parts[:i])  # Construct the file name (e.g., "base", "base_eu", etc.)
        file_path = Path(config_folder) / Path(f"{config_file}.json")

        # Ensure the file exists
        if not Path.exists(file_path):
            raise FileNotFoundError(f"Config file not found: {file_path}")

        # Read and merge the JSON data from the file
        with Path.open(file_path) as f:
            data = json.load(f)
            merged_data.update(data)

    return merged_data


def load_data():
    folder_path = Path("../python-syml/data")
    files = os.listdir(folder_path)

    # Filter files to find CSV and Parquet files
    csv_files = [f for f in files if f.endswith(".csv")]
    parquet_files = [f for f in files if f.endswith(".parquet")]

    # Check if there is exactly one CSV or Parquet file
    if len(csv_files) + len(parquet_files) != 1:
        raise ValueError("There should be exactly one CSV or Parquet file in the folder.")

    # Determine the file to read
    if csv_files:
        file_path = folder_path / Path(csv_files[0])
        df = pd.read_csv(file_path)
    elif parquet_files:
        file_path = folder_path, Path(parquet_files[0])
        df = pd.read_parquet(file_path)

    return df
