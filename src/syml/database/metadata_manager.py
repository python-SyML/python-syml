import json

import Path


class JSONFileHandler:
    def __init__(self, file_path):
        self.file_path = Path(file_path)

    def create_json_file(self, data):
        """
        Create a JSON file with the given data.

        :param data: Dictionary or list to be written to the JSON file.
        """
        with self.file_path.open("w") as file:
            json.dump(data, file, indent=4)

    def read_json_file(self):
        """
        Read data from the JSON file.

        :return: Dictionary or list containing the data from the JSON file.
        """
        if not self.file_path.exists():
            print(f"File '{self.file_path}' does not exist.")
            return None

        with self.file_path.open() as file:
            data = json.load(file)
        return data

    def write_json_file(self, data):
        """
        Write data to the JSON file.

        :param data: Dictionary or list to be written to the JSON file.
        """
        with self.file_path.open("w") as file:
            json.dump(data, file, indent=4)

    def append_to_json_file(self, data):
        """
        Append data to the JSON file.

        :param data: Dictionary or list to be appended to the JSON file.
        """
        existing_data = self.read_json_file()
        if existing_data is None:
            existing_data = []

        if isinstance(existing_data, list):
            existing_data.append(data)
        elif isinstance(existing_data, dict):
            existing_data.update(data)
        else:
            return

        self.write_json_file(existing_data)