import streamlit as st

from syml.interract.field_inspector import FieldInspector

from .utils import read_data


class Dashboard:
    def __init__(self, path, nrows=None) -> None:
        self.dataset = read_data(path, nrows)
        self.field_inspector = FieldInspector()

    def display(self):
        data = self.dataset

        self.introduction()
        self.data_explorer(data)

        self.field_inspector.display(data)

    def introduction(self):
        st.title("SyML Dashboard :bar_chart:")

        st.markdown("""
                    **Welcome to SyML Dashboard !**

                    Thank you for dowloading SyML. Let us explain how it works.
                    SyML is a python library that provides several NLP, ML and xAI services encapsulated within a nice UI.
                    SyML aims to make data preparation, ML training and xAI usage the simplest possible.

                    On this page, you'll find below a few exploratory components to understand better your data. For more advanced features,
                    you can use the navigation menu to visit the other modules of SyML.

                    First, you can have a look at a sample of your dataset. Then, the **Field Inspector** :microscope: will help you understand
                    each field of your dataset :
                    - basic summarized information at first, like the data type,
                    - advanced information, like the variability, min-max values, etc.
                    """)

    def data_explorer(self, data):
        st.divider()
        st.header("Dataset overview")
        checkbox = st.checkbox("Display Raw Dataset")

        if checkbox:
            st.dataframe(data)
