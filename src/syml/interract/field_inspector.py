import numpy as np
import pandas as pd
import streamlit as st

from syml.diagnostool.calculator import data_profiler
from syml.diagnostool.calculator import variability_calculator


class FieldInspector:
    def __init__(
        self,
    ):
        pass

    def display(self, data: pd.DataFrame):
        st.divider()
        st.header("Field Inspector :microscope:")

        self.introduction()
        # Display basic information (type, completion) about the different fields in the table.
        df = data_profiler(data)
        self.basic_summary(profiled_data=df)
        self.advanced_analysis(data=data)

    def introduction(self):
        st.markdown("""
                    The **Field Inspector** :mag: will help you understand your data on a technical level.
                    The goal is to provide you with information about the type, the completion, the variability and
                    other characteristics that will help you diagnose the quality of your data.

                    Once you'll have a better understanding of your raw data, **:blue[QIA]** (Quality Improvement Assistant) will help you boost your
                    data coverage, quality and uniformity.

                    Then, with the help of **:orange[ADA]** (Advanced Data Analyst) you will get a deep comprehension of relationships and patterns in your data.
                    """)

    def basic_summary(self, profiled_data: pd.DataFrame):
        st.subheader("Basic summary :mag:")
        st.markdown("""The following table contains a basic summary about your data.
                    You'll see the field completion, the detected data type and the field name.
                    """)

        st.data_editor(
            profiled_data,
            hide_index=True,
            column_config={
                "field names": st.column_config.TextColumn(
                    "field names",
                    disabled=True,
                ),
                "data type": st.column_config.TextColumn(
                    "data type",
                    help="Data is either Continuous (length, amount of money, ...) or Categorical (gender, name of a color, ...)",
                ),
                "field completion": st.column_config.ProgressColumn(
                    "field completion",
                    help="percentage of rows that contain a value for each field",
                    format="%.0f",
                    min_value=0,
                    max_value=100,
                ),
            },
        )

    def advanced_analysis(self, data):
        st.subheader("Advanced Analysis :microscope:")
        st.markdown("""The Advanced Analysis section helps you diagnose problems in your raw data.
                    For example, it can happen that you have outliers in your continuous data, or you
                    could have for a categorical variable a very large number of labels due to typos.
                    """)

        variability = variability_calculator(data)

        if "continuous" in variability.keys():
            st.markdown("""
                        #### Continuous Variables
                        Continuous variables are analyzed below.
                        Each field has been normalized by its mean, allowing to compare the spread and the min-max values.
                        """)

            data_hist = {"values": []}
            for field in variability["continuous"].columns:
                hist, bin_edges = np.histogram(data[field].tolist(), bins=20)
                data_hist["values"].append(hist)
            data_hist = pd.DataFrame(data_hist, index=variability["continuous"].columns)

            table = pd.concat([variability["continuous"].T, data_hist], axis=1)

            st.data_editor(
                table,
                column_config={
                    "values": st.column_config.BarChartColumn(
                        "Histogram",
                        help="Histogram of the values of each field",
                        width="medium",
                    ),
                },
                hide_index=False,
                disabled=True,
            )

        if "categorical" in variability.keys():
            st.markdown("""
                        #### Categorical Variables
                        Categorical variables are analyzed below.
                        For each field the occurrence of each unique label has been counted, then a few statistics are computed :
                        - number of distinct labels
                        - average occurrence of a label
                        - min-max occurrence of label
                        """)

            st.table(variability["categorical"])
