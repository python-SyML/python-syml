import streamlit as st

from syml.interract.page_class import BasePageElement

from .categorical_components.label_grouping import LabelGrouping


class CategoricalQIA(BasePageElement):
    def __init__(
        self,
        data=None,
        name="Categical Quality Improvement Assistant",
    ):
        self.name = name
        self.data = data
        super().__init__()

    def setup(self):
        self.setup_child(LabelGrouping(self.data))

    def introduction(self):
        st.header("I. Categorical Quality Improvement Assistant")

        st.markdown("""
                    The C-QIA aims to help you setup robust methods to
                    improve data quality for categorical data. First it aims to diagnose
                    precisely your data issues and then using NLP techniques you will be able
                    to automatically correct these issues.

                    The current main components of C-QIA are :
                    - label identification
                    - label typo correction
                    - label grouping
                    - missing label extraction
                    - color name extraction
                    """)
