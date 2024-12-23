import streamlit as st

from syml.interract.page_class import BasePageElement


class LabelGrouping(BasePageElement):
    def __init__(self, data=None, name="Label Grouping"):
        self.name = name
        self.data = data

        super().__init__()

    def setup(self):
        pass

    def introduction(self):
        st.subheader("II. A. Label Grouping")

        st.markdown("""
                    The goal of this step is to group similar labels together,
                    to make the data easier to understand and manage.
                    """)

    def analysis(self):
        pass
