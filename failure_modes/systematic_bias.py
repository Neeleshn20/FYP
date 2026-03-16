import numpy as np

def apply(df, bias_strength=0.35, biased_stores=None):

    df_new = df.copy()

    # If no stores specified, bias ALL stores
    if biased_stores is None:
        biased_stores = df_new["Store"].unique()

    # Apply bias store-by-store
    for store in biased_stores:

        mask = df_new["Store"] == store

        df_new.loc[mask, "allocated_inventory"] *= (1 + bias_strength)

    # Recalculate downstream variables
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