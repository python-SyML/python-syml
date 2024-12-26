from sklearn.datasets import fetch_openml

from syml.database.sql_database import SQLDatabase
from syml.interract.discovery_dashboard.dashboard import Dashboard

if __name__ == "__page__":
    data = fetch_openml("adult", version=2).data
    data.to_csv("../python-syml/data/dataset.csv")
    db = SQLDatabase(db_path="../python-syml/data/database.db", metadata_path="../python-syml/config/metadata.json")
    csv_file = "../python-syml/data/dataset.csv"
    _ = db.generate_database(csv_file=csv_file, table_name="dataset")
    dash = Dashboard(db)
    dash.display()
