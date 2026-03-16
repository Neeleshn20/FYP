import numpy as np

def apply(df, severity=0.30, priority_depts=[1,2,3,4,5]):

    df_new = df.copy()

    mask = df_new["Dept"].isin(priority_depts)

    df_new.loc[mask, "allocated_inventory"] *= (1 + severity)

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
        np.minimum(
            df_new["allocated_inventory"],
            df_new["Weekly_Sales"]
        ) / (df_new["Weekly_Sales"] + epsilon)
    )

    return df_new