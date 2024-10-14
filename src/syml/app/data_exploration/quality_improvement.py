import pandas as pd
from sklearn.datasets import fetch_openml

from syml.interract.quality_improvement.quality_report import Report

if __name__ == "__page__":
    data = fetch_openml("adult", version=2)
    df = pd.DataFrame(data=data.data, columns=data.feature_names)
    rpt = Report(df)
    rpt.display()
