import pandas as pd
from sklearn.datasets import fetch_openml
from sklearn.datasets import load_iris

from syml.interract.discovery_dashboard.dashboard import Dashboard

if __name__ == "__page__":
    data = load_iris()
    data = fetch_openml("adult", version=2)
    df = pd.DataFrame(data=data.data, columns=data.feature_names)
    dash = Dashboard(df)
    dash.display()
