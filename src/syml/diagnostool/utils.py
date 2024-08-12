import pandas as pd


def classify_columns(df: pd.DataFrame) -> dict:
    """
    Classify each column in the DataFrame as categorical or continuous.

    Parameters:
    df (pd.DataFrame): The DataFrame to classify.

    Returns:
    dict: A dictionary with column names as keys and 'categorical' or 'continuous' as values.
    """
    classification = {}

    for col in df.columns:
        inferred_dtype = pd.api.types.infer_dtype(df[col], skipna=True)

        if inferred_dtype in ["string", "unicode", "mixed-integer", "mixed", "mixed-integer-float", "integer"]:
            classification[col] = "categorical"
        elif inferred_dtype in ["floating", "decimal"]:
            classification[col] = "continuous"
        else:
            classification[col] = "unknown"  # For types that don't clearly fall into either category

    return classification
