import pandas as pd
from sklearn.datasets import load_iris

from syml.interract.dashboard import Dashboard


def compute(args):
    return max(args, key=len)


if __name__ == "__main__":
    data = load_iris()
    df = pd.DataFrame(data=data.data, columns=data.feature_names)
    dash = Dashboard(df)
    dash.display()
