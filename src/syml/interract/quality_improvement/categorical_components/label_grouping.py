import pandas as pd
import streamlit as st

from syml.diagnostool.semantic.semantIA import SementIA
from syml.diagnostool.semantic.utils import df_typo
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
        columns = self.data.columns
        to_inspect = st.selectbox("Field to inspect :mag:", options=columns)
        data = pd.DataFrame(self.data[to_inspect].dropna().value_counts())

        st.markdown("""
                    If you want to simulate potential typos in your data in order to further be able to prevent those,
                    activate the following setting. This will generate random typos in the labels. You can also
                    select the number of typos per label you want to simulate.
                    """)
        on = st.toggle("Activate Typos Simulation ☢️")
        if on:
            st.markdown("""
                        Chose the number of typos per label to simulate below :
                        """)

            n_typos = st.slider("Number of typos", 1, 20, step=1, value=5)
            data = df_typo(data, n_typos=n_typos)

        label_analysis = SementIA(data=data, path="../python-syml/data/embeddings_{field_name}.pt", field_name=to_inspect)
        clusters = label_analysis.embedder.clustering.clusters

        fig = label_analysis.scatter_labels()
        st.plotly_chart(fig)

        fig = label_analysis.heatmap_similiarities()
        st.plotly_chart(fig)

        tabs = st.tabs(clusters.keys())

        for tab, labels_clustered in zip(tabs, clusters.values()):
            tab.write("Cluster contains the following values :")
            tab.write(labels_clustered)
