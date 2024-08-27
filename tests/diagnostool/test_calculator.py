import pandas as pd

from syml.diagnostool.calculator import data_profiler
from syml.diagnostool.calculator import variability_calculator
from syml.diagnostool.utils import categorical_variability
from syml.diagnostool.utils import continuous_variability


def test_data_profiler_with_iris(iris_dataframe):
    """
    Test the data_profiler function using the Iris dataset.
    """
    result = data_profiler(iris_dataframe)

    # Expected field names
    expected_fields = ["sepal length (cm)", "sepal width (cm)", "petal length (cm)", "petal width (cm)", "target"]

    # Expected data types
    expected_types = {
        "sepal length (cm)": "continuous",
        "sepal width (cm)": "continuous",
        "petal length (cm)": "continuous",
        "petal width (cm)": "continuous",
        "target": "categorical",
    }

    # Check the structure of the result DataFrame
    assert isinstance(result, pd.DataFrame), "The result should be a pandas DataFrame"
    assert list(result.columns) == [
        "field names",
        "data type",
        "field completion",
        "examples",
    ], "DataFrame should have columns: 'field names', 'data type', 'field completion', 'examples'"

    # Check the field names
    assert list(result["field names"]) == expected_fields, f"Expected fields {expected_fields} but got {list(result['field names'])}"

    # Check the data types
    assert list(result["data type"]) == list(
        expected_types.values()
    ), f"Expected data types {list(expected_types.values())} but got {list(result['data type'])}"

    # Check field completion (Iris dataset should be 100% complete)
    assert all(result["field completion"] == 100.0), "All fields should be 100% complete"

    # Additional checks can be added here, e.g., for variance if the function is extended


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
