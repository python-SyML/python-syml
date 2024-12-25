import pandas as pd
from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class SQLDatabase:
    def __init__(self, csv_file="", db_uri="sqlite:///../data/database.db"):
        self.engine = create_engine(db_uri)
        self.csv_file = csv_file
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.Base = declarative_base()

    def read_csv(self):
        self.df = pd.read_csv(self.csv_file)

    def create_table_schema(self):
        class DynamicTable(self.Base):
            __tablename__ = "dynamic_table"
            id = Column(Integer, primary_key=True, autoincrement=True)

        for column in self.df.columns:
            col_type = self.df[column].dtype
            if col_type == "int64":
                col_type = Integer
            elif col_type == "float64":
                col_type = Float
            else:
                col_type = String
            setattr(DynamicTable, column, Column(col_type))

        self.DynamicTable = DynamicTable
        self.Base.metadata.create_all(self.engine)

    def insert_data(self):
        for _index, row in self.df.iterrows():
            data = {column: row[column] for column in self.df.columns}
            new_record = self.DynamicTable(**data)
            self.session.add(new_record)
        self.session.commit()

    def close_session(self):
        self.session.close()

    def generate_database(self):
        self.read_csv()
        self.create_table_schema()
        self.insert_data()
        self.close_session()
