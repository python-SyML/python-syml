import pandas as pd

from syml.diagnostool.utils import categorical_variability
from syml.diagnostool.utils import categorical_variability_serie
from syml.diagnostool.utils import classify_columns
from syml.diagnostool.utils import continuous_variability
from syml.diagnostool.utils import variability_calculator


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


def test_variability_calculator(iris_dataframe, monkeypatch):
    # Mocking classify_columns function
    def mock_classify_columns(df):
        return pd.Series(
            ["continuous" if dtype.kind in "fc" else "categorical" for dtype in df.dtypes],
            index=df.columns,
        )

    # Patch the classify_columns function
    monkeypatch.setattr("syml.diagnostool.utils", mock_classify_columns)

    result = variability_calculator(iris_dataframe)

    # Ensure keys are present in the result
    assert "continuous" in result
    assert "categorical" in result
    # Check if the continuous variability results are as expected
    continuous_df = iris_dataframe.select_dtypes(include=[float])
    expected_continuous = continuous_variability(continuous_df)
    pd.testing.assert_frame_equal(result["continuous"], expected_continuous)

    # Check if the categorical variability results are as expected
    categorical_df = iris_dataframe.select_dtypes(exclude=[float])
    expected_categorical = categorical_variability(categorical_df)
    pd.testing.assert_frame_equal(result["categorical"], expected_categorical)


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


def test_continuous_variability(iris_dataframe):
    # Filter out continuous columns
    continuous_df = iris_dataframe.select_dtypes(include=[float, int])

    result = continuous_variability(continuous_df)

    # Verify the structure of the result
    assert "normalized standard deviation" in result.columns

    # Ensure the calculation is correct
    expected = continuous_df.std() / continuous_df.mean()
    expected.name = "normalized standard deviation"

    pd.testing.assert_series_equal(result["normalized standard deviation"], expected)


def test_categorical_variability_serie(iris_dataframe):
    # Extract a sample categorical column
    serie = iris_dataframe["target"].astype(str)  # Assuming "target" is categorical

    result = categorical_variability_serie(serie)

    # Verify the structure of the result
    expected_stats = ["count", "mean", "std", "min", "25%", "50%", "75%", "max"]
    assert all(stat in result.index for stat in expected_stats)

    # Additional checks can be performed based on the expected behavior
