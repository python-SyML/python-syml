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
        st.subheader("I. A. Proof Reading is a must")

        st.markdown("""
                    Too often data is badly labeled : typos, inconsistent label format, excessive variety of labels, etc. First and foremost, we must correct typos and incorrect spelling.
                    This is exactly what this submodule will help you achieve.

                    This submodule will help you :
                    - identify what are the true different labels,
                    - link the labels with typos to the original ones,

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

        st.markdown("""
                    #### Labels clusters

                    Here are the labels clustered based on Levenshtein ratios and transformers embeddings.
                    """)

        tabs = st.tabs(clusters.keys())

        for tab, labels_clustered in zip(tabs, clusters.values()):
            tab.write("Cluster contains the following values :")
            tab.write(labels_clustered)

        st.markdown("""
                    #### Scatter plot of labels

                    This scatter plot will help you visualize the distance between labels.
                    Beware that this is a 2D scatter plot of SBERT embeddings which are in a much higher dimensional space.
                    Because we are using SBERT embeddings, the distance between labels corresponds to
                    the semantic proximity of the strings. However, if there are typos, this tool may not be
                    very realiable.

                    Data points are colored by cluster.
                    """)
        fig = label_analysis.scatter_labels()
        st.plotly_chart(fig)

        st.markdown("""
                #### Similarity matrix of labels

                This heatmap will help you visualize the similarity between labels. It is based on the levenshtein ratio and the cosine similarity
                between SBERT embeddings.
                """)

        fig = label_analysis.heatmap_similiarities()
        st.plotly_chart(fig)
