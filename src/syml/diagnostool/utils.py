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

    return pd.Series(classification, name="data type")


def variability_calculator(df: pd.DataFrame):
    classification = classify_columns(df)
    variability = {}

    if "continuous" in classification.values:
        continous_cols = df[classification[classification == "continuous"].index]
        continuous_var = continuous_variability(continous_cols)
        variability["continuous"] = continuous_var

    if "categorical" in classification.values:
        categorical_cols = df[classification[classification == "categorical"].index]
        categorical_var = categorical_variability(categorical_cols)
        variability["categorical"] = categorical_var

    return variability


def categorical_variability(df: pd.DataFrame):
    var = df.apply(categorical_variability_serie, axis=0)
    var = var.drop(["25%", "50%", "75%"]).T
    var = var.rename(
        columns={
            "mean": "average number of occurrence of a label",
            "count": "number of unique labels",
            "min": "minimum number of occurrences of a label",
            "max": "maximum number of occurrences of a label",
        }
    )
    return var


def continuous_variability(df: pd.DataFrame):
    var = df.std() / df.mean()
    var = pd.DataFrame(var, columns=["normalized standard deviation"])
    return var


def categorical_variability_serie(s: pd.Series):
    val_occurrence = s.value_counts()
    var = val_occurrence.describe()
    return var
