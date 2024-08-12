import streamlit as st

from syml.diagnostool.calculator import data_profiler

from .utils import read_data


class Dashboard:
    def __init__(self, path, nrows=None) -> None:
        self.dataset = read_data(path, nrows)

    def display(self):
        data = self.dataset

        st.title("SyML Dashboard")
        st.header("Dataset overview")

        checkbox = st.checkbox("Display Raw Dataset")

        if checkbox:
            st.dataframe(data)

        st.subheader("Field Inspector")

        df = data_profiler(data)

        st.data_editor(
            df,
            hide_index=True,
            column_config={
                "field names": st.column_config.TextColumn(
                    "field names",
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
