import streamlit as st

from syml.interract.page_class import BasePageElement


class LabelGrouping(BasePageElement):
    def __init__(self, data=None, name="Label Grouping"):
        self.name = name
        self.data = data

        super().__init__()

    def setup(self):
        self.actions += [self.analysis]

    def introduction(self):
        st.subheader("I. A. Label identification, correction and grouping")

        st.markdown("""
                    The goal of this step is to :
                    - identify what are the true different labels,
                    - group similar labels together,
                    - and remove typos.

                    This will make the data easier to understand and manage.

                    First of all, select the categorical field you want to work on.
                    """)

    def analysis(self):
        # TODO: Implement the label grouping and correction logic here using the notebook
        # data = self.data
        # to_inspect = st.selectbox("Field to inspect :mag:", options=data)
        pass
