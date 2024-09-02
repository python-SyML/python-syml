import streamlit as st

from syml.interract.page_class import BasePageElement
from syml.interract.utils import read_data

from .field_inspector import FieldInspector


class Dashboard(BasePageElement):
    def __init__(self, path, nrows=None) -> None:
        self.dataset = read_data(path, nrows)
        super().__init__()

    def setup(self):
        self.actions.append(self.data_explorer)
        self.setup_child(FieldInspector(self.dataset))

    def introduction(self):
        st.title("Data Discovery Dashboard :telescope:")

        st.markdown("""
                    **Welcome to the 3D world !**

                    On this page, you'll find below a few exploratory components to understand better your data. For more advanced features,
                    you can use the navigation menu to visit the other modules of SyML.

                    First, you can have a look at a sample of your dataset. Then, the **Field Inspector** :microscope: will help you understand
                    each field of your dataset :
                    - basic summarized information at first, like the data type,
                    - advanced information, like the variability, min-max values, etc.
                    """)

    def data_explorer(self):
        st.divider()
        st.header("Dataset overview")
        checkbox = st.checkbox("Display Raw Dataset")

        if checkbox:
            st.dataframe(self.dataset)
