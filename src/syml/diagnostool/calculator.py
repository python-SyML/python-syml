import pandas as pd

from .utils import classify_columns


def data_profiler(data):
    field_data = pd.Series(data.columns, name="field names")
    field_type = pd.Series(classify_columns(data), name="data type").reset_index(drop=True)
    fillage_data = 100 * pd.Series([data[col].notna().sum() / len(data) for col in field_data], name="field completion")

    # data_variability = {col: data[col].nunique(dropna=True) for col in field_data}

    df = pd.concat([field_data, field_type, fillage_data], axis=1)

    return df
