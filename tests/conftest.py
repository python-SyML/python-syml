import pytest
from sklearn.datasets import load_iris


@pytest.fixture(scope="module")
def iris_dataframe():
    """
    Fixture that provides a pandas DataFrame with the Iris dataset.
    """
    iris = load_iris(as_frame=True)
    df = iris.frame
    return df
