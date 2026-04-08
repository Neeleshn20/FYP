import numpy as np
from failure_modes.utils import recompute_supply_metrics

def apply(df, lookback_weeks=1):

    df_new = df.copy()

    df_new = df_new.sort_values(["Store", "Dept", "Date"])

    df_new["expected_demand"] = (
        df_new.groupby(["Store", "Dept"])["Weekly_Sales"]
        .rolling(lookback_weeks)
        .mean()
        .reset_index(level=[0,1], drop=True)
    )

    df_new["expected_demand"].fillna(df_new["Weekly_Sales"], inplace=True)

    df_new["allocated_inventory"] = df_new["expected_demand"]

    return recompute_supply_metrics(df_new)