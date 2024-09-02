import streamlit as st

from syml.interract.page_class import BasePageElement

from .field_analysts import AdvancedAnalysis
from .field_analysts import BasicAnalysis


class FieldInspector(BasePageElement):
    def __init__(
        self,
        data=None,
        name="FieldInspector",
    ):
        self.name = name
        self.data = data
        super().__init__()

    def setup(self):
        self.setup_child(child=BasicAnalysis(data=self.data))
        self.setup_child(child=self.setup_advanced_analysis())

    def introduction(self):
        st.header("II. Field Inspector :microscope:")
        st.markdown("""
                    The **Field Inspector** :microscope: will help you understand your data on a technical level.
                    The goal is to provide you with information about the type, the completion, the variability and
                    other characteristics that will help you diagnose the quality of your data.

                    Once you'll have a better understanding of your raw data, **:blue[QIA]** (Quality Improvement Assistant) will help you boost your
                    data coverage, quality and uniformity.

                    Then, with the help of **:orange[ADA]** (Advanced Data Analyst) you will get a deep comprehension of relationships and patterns in your data.
                    """)

    def setup_advanced_analysis(self):
        classification = self.children["BasicAnalysis"].classification
        adv_analysis = AdvancedAnalysis(data=self.data, classification=classification)
        return adv_analysis
