import numpy as np

def apply(df, severity=0.25, cluster_size=10):

    df_new = df.copy()

    cluster_stores = df_new["Store"].unique()[:cluster_size]

    mask = df_new["Store"].isin(cluster_stores)

    df_new.loc[mask, "Weekly_Sales"] *= (1 + severity)

    # recompute consequences
    df_new["fulfilled_demand"] = np.minimum(
        df_new["allocated_inventory"],
        df_new["Weekly_Sales"]
    )

    df_new["unmet_demand"] = np.maximum(
        0,
        df_new["Weekly_Sales"] - df_new["allocated_inventory"]
    )

    df_new["overstock"] = np.maximum(
        0,
        df_new["allocated_inventory"] - df_new["Weekly_Sales"]
    )

    epsilon = 1e-6

    df_new["service_level"] = (
        df_new["fulfilled_demand"] /
        (df_new["Weekly_Sales"] + epsilon)
    )

    return df_new