import pandas as pd
import streamlit as st

from syml.diagnostool.calculator import data_profiler


class FieldInspector:
    def __init__(
        self,
    ):
        pass

    def display(self, data: pd.DataFrame):
        st.divider()
        st.subheader("Field Inspector :microscope:")

        # Display basic information (type, completion) about the different fields in the table.
        df = data_profiler(data)
        self.basic_summary(profiled_data=df)

    def basic_summary(self, profiled_data: pd.DataFrame):
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
