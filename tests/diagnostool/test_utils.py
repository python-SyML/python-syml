import pandas as pd

from syml.diagnostool.utils import categorical_variability
from syml.diagnostool.utils import categorical_variability_serie
from syml.diagnostool.utils import classify_columns
from syml.diagnostool.utils import continuous_variability


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
        "target": "continuous",
    }

    expected = pd.Series(expected)

    assert (result == expected).all(), f"Expected {expected} but got {result}"


def test_continuous_variability(iris_dataframe):
    # Filter out continuous columns
    continuous_df = iris_dataframe.select_dtypes(include=[float, int])

    result = continuous_variability(continuous_df)

    # Verify the structure of the result
    assert (continuous_df.columns == result.columns).all()

    # Ensure the calculation is correct
    expected = continuous_df
    expected = expected.describe().drop(["25%", "50%", "75%"])

    pd.testing.assert_frame_equal(result, expected)


def test_categorical_variability(iris_dataframe):
    # Create a sample categorical DataFrame
    df = pd.DataFrame(
        {
            "species": iris_dataframe["target"].astype(str)  # Assuming "target" is categorical
        }
    )

    result = categorical_variability(df)

    # Verify the structure of the result
    assert "average number of occurrence of a label" in result.columns
    assert "number of unique labels" in result.columns
    assert "minimum number of occurrences of a label" in result.columns
    assert "maximum number of occurrences of a label" in result.columns

    # Additional checks can be performed based on the expected behavior


def test_categorical_variability_serie(iris_dataframe):
    # Extract a sample categorical column
    serie = iris_dataframe["target"].astype(str)  # Assuming "target" is categorical

    result = categorical_variability_serie(serie)

    # Verify the structure of the result
    expected_stats = ["count", "mean", "std", "min", "25%", "50%", "75%", "max"]
    assert all(stat in result.index for stat in expected_stats)

    # Additional checks can be performed based on the expected behavior
