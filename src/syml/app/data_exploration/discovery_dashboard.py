import pandas as pd
from sklearn.datasets import load_iris

from syml.interract.dashboard import Dashboard

if __name__ == "__page__":
    data = load_iris()
    df = pd.DataFrame(data=data.data, columns=data.feature_names)
    dash = Dashboard(df)
    dash.display()
