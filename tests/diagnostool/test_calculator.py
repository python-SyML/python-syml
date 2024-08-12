import pandas as pd

from syml.diagnostool.calculator import data_profiler


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
    ], "DataFrame should have columns: 'field names', 'data type', 'field completion'"

    # Check the field names
    assert list(result["field names"]) == expected_fields, f"Expected fields {expected_fields} but got {list(result['field names'])}"

    # Check the data types
    assert list(result["data type"]) == list(
        expected_types.values()
    ), f"Expected data types {list(expected_types.values())} but got {list(result['data type'])}"

    # Check field completion (Iris dataset should be 100% complete)
    assert all(result["field completion"] == 100.0), "All fields should be 100% complete"

    # Additional checks can be added here, e.g., for variance if the function is extended
