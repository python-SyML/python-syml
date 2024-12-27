import pandas as pd
import streamlit as st


@st.cache_data
def read_data(path, nrows=None):
    if isinstance(path, pd.DataFrame):
        df = path
    else:
        df = pd.read_csv(path)

    if isinstance(nrows, int):
        df = df.head(int)
    elif isinstance(nrows, float):
        df = df.head(int(float) * len(df))
    elif nrows is not None:
        raise TypeError("nrows must be an integer or float")

    return df
