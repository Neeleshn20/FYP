import numpy as np

def apply(df, severity=0.3, dept_count=5):

    df_new = df.copy()

    coupled_depts = df_new["Dept"].unique()[:dept_count]

    mask = df_new["Dept"].isin(coupled_depts)

    oscillation = np.sin(np.linspace(0, 10, mask.sum()))

    df_new.loc[mask, "Weekly_Sales"] *= (
        1 + severity * oscillation
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
        np.minimum(
            df_new["allocated_inventory"],
            df_new["Weekly_Sales"]
        ) / (df_new["Weekly_Sales"] + epsilon)
    )

    return df_new