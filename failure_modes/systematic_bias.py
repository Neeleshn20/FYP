from failure_modes.utils import recompute_supply_metrics

def apply(df, bias_strength=0.35, biased_stores=None):

    df_new = df.copy()

    if biased_stores is None:
        biased_stores = df_new["Store"].unique()

    for store in biased_stores:

        mask = df_new["Store"] == store

        df_new.loc[mask, "allocated_inventory"] *= (1 + bias_strength)

    return recompute_supply_metrics(df_new)