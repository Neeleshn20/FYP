# failure_modes/utils.py

import numpy as np

def recompute_supply_metrics(df):

    df["unmet_demand"] = np.maximum(
        0,
        df["Weekly_Sales"] - df["allocated_inventory"]
    )

    df["overstock"] = np.maximum(
        0,
        df["allocated_inventory"] - df["Weekly_Sales"]
    )

    df["service_level"] = np.where(
        df["Weekly_Sales"] > 0,
        np.minimum(1, df["allocated_inventory"] / df["Weekly_Sales"]),
        1
    )

    return df