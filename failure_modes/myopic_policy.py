import numpy as np

def apply(df, lookback_weeks=1):

    df_new = df.copy()

    df_new = df_new.sort_values(["Store", "Dept", "Date"])

    # Myopic demand estimate using rolling window
    df_new["expected_demand"] = (
        df_new
        .groupby(["Store", "Dept"])["Weekly_Sales"]
        .rolling(lookback_weeks)
        .mean()
        .reset_index(level=[0,1], drop=True)
    )

    # Fill early weeks where rolling window is incomplete
    df_new["expected_demand"] = df_new["expected_demand"].fillna(df_new["Weekly_Sales"])

    # Allocation follows the forecast
    df_new["allocated_inventory"] = df_new["expected_demand"]

    # Recompute supply chain outcomes
    df_new["unmet_demand"] = np.maximum(
        0,
        df_new["Weekly_Sales"] - df_new["allocated_inventory"]
    )

    df_new["overstock"] = np.maximum(
        0,
        df_new["allocated_inventory"] - df_new["Weekly_Sales"]
    )

    df_new["service_level"] = np.where(
        df_new["Weekly_Sales"] > 0,
        np.minimum(
            1,
            df_new["allocated_inventory"] / df_new["Weekly_Sales"]
        ),
        1
    )

    return df_new