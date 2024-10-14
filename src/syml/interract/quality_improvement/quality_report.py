import streamlit as st

from syml.interract.page_class import BasePageElement
from syml.interract.utils import read_data

from .categorical_qia import CategoricalQIA


class Report(BasePageElement):
    def __init__(self, path, nrows=None) -> None:
        self.dataset = read_data(path, nrows)
        super().__init__()

    def setup(self):
        self.setup_child(CategoricalQIA(self.dataset))

    def introduction(self):
        st.title("Quality Improvement Assistant 🧑🏼‍🔬")

        st.markdown("""
                    **You can do better !**

                    #### Introduction

                    On this page you'll find powerful modules to help you mitigate potential data quality issues, such as :
                    - Badly labeled data
                    - typos in categorical data
                    - missing values
                    - anormal extreme numerical data
                    - ... and many other !
                    """)
