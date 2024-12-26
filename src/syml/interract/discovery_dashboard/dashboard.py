import streamlit as st

from syml.interract.page_class import BasePageElement

from ...database.sql_database import SQLDatabase
from .field_inspector import FieldInspector


class Dashboard(BasePageElement):
    def __init__(self, db_path="../python-syml/data/database.db") -> None:
        sql_db = SQLDatabase(db_path=db_path, metadata_path="../python-syml/config/metadata.json")
        self.data = sql_db.query("SELECT * FROM dataset")
        super().__init__()

    def setup(self):
        self.actions.append(self.data_explorer)
        self.setup_child(FieldInspector(self.data))

    def introduction(self):
        st.title("Data Discovery Dashboard :telescope:")

        st.markdown("""
                    **Welcome to the 3D world !**

                    #### Introduction

                    On this page, you'll find below a few exploratory components to understand better your data. For more advanced features,
                    you can use the navigation menu to visit the other modules of SyML.
                    This page is **not** meant to analyze relationships and hidden structures in your data.
                    It is meant to help you get a sense of the quality of your data : find out if you have labelling issues in categorical field,
                    potential outliers or very abnormal distributions of continuous data.

                    ##### Look at your data !

                    First, have a look at a sample of your dataset. It is always good to take a quick look at the data to get a better sense of the quality,
                    but also what each field means. It is very important to know what each field is supposed to contain, as the data quality issues that you may
                    expect depends heavily on it.

                    ##### Motivation : a real world example.

                    Just an example : imagine a field "bottle volume" in which you have some data in liters and some in militers for bottles of water.
                    This is a good example of a data quality issue related to different unit systems. It is very common in companies, and happens very often especially
                    between different countries with different unit systems. **How would you diagnose such an issue?**

                    The goal of the tool is to highlight those descrepencies so you can identify them. The resulting distribution will be a complete mess :
                    you will see a huge delta between the min and max values, the histogram will show probably two normal distributions
                    centered around 1e3 and the other around 1.
                    - If you are aware that this field contains volumes of bottles, and you have a bit of business knowledge
                    of the type of product the company sells, then you will understand that this double normal distribution is the result of a data quality issue.
                    From there, you'll be able to treat those issues with other tools from SyML. You could build a robust
                    process that will automatically rescale the values to the same unit system.
                    - If not, you may chose to discard one of the "faulty" distribution, resulting in a loss of data,
                    and a decrease in performance for your ML models based on that data.
                    Or you could keep the data as it is, and risk again a decrease of your ML model's performances.

                    ##### Our inspection tools.

                    The **Field Inspector** :microscope: will help you understand the quality level of each field of your dataset.
                    - The basic analysis will give you summarized information about the data completeness and type.
                    - The advanced analysis provides more detailed information, statistics and charts on the data.
                    """)

    def data_explorer(self):
        st.divider()
        st.header("I. Dataset overview")
        checkbox = st.checkbox("Display Raw dataset")

        if checkbox:
            st.dataframe(self.data)
