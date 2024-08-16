import pandas as pd

from .utils import classify_columns


def data_profiler(data):
    """
    This function is responsible for profiling the raw data given to syml.

    It returns basic information about the data, for each field :
     - detected type (continuous, categorical or unknown)
     - percentage of completion
     - variance
     - ...

    Args:
        data (pd.DataFrame): the raw  data to be profiled.

    Returns:
        pd.DataFrame: The result of the profiling.
    """
    field_data = pd.Series(data.columns, name="field names")
    field_type = classify_columns(data).reset_index(drop=True)
    fillage_data = 100 * pd.Series([data[col].notna().sum() / len(data) for col in field_data], name="field completion")

    df = pd.concat([field_data, field_type, fillage_data], axis=1)

    return df
