import pandas as pd

def apply(df, delay_weeks=4):

    df_delayed = df.copy()

    df_delayed["expected_demand"] = (
        df_delayed
        .groupby(["Store", "Dept"])["expected_demand"]
        .shift(delay_weeks)
    )

    df_delayed = df_delayed.dropna().reset_index(drop=True)

    return df_delayed
