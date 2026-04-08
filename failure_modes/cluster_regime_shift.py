from failure_modes.utils import recompute_supply_metrics

def apply(df, severity=0.25, cluster_size=10):

    df_new = df.copy()

    cluster_stores = df_new["Store"].unique()[:cluster_size]

    mask = df_new["Store"].isin(cluster_stores)

    df_new.loc[mask, "Weekly_Sales"] *= (1 + severity)

    return recompute_supply_metrics(df_new)