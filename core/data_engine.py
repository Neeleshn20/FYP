import pandas as pd

def load_data(path="outputs/phase1_decisions.csv"):
    df = pd.read_csv(path)
    df["Date"] = pd.to_datetime(df["Date"])
    return df