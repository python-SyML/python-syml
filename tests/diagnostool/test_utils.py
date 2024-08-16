import pandas as pd

from syml.diagnostool.utils import classify_columns


def test_classify_columns_with_iris(iris_dataframe):
    """
    Test classify_columns function using the Iris dataset.
    """
    result = classify_columns(iris_dataframe)

    # The Iris dataset contains:
    # - 'sepal length (cm)' : continuous
    # - 'sepal width (cm)'  : continuous
    # - 'petal length (cm)' : continuous
    # - 'petal width (cm)'  : continuous
    # - 'target'            : categorical

    expected = {
        "sepal length (cm)": "continuous",
        "sepal width (cm)": "continuous",
        "petal length (cm)": "continuous",
        "petal width (cm)": "continuous",
        "target": "categorical",
    }

    expected = pd.Series(expected)

    assert (result == expected).all(), f"Expected {expected} but got {result}"
