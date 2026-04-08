from failure_modes.utils import recompute_supply_metrics

def apply(df, severity=0.30, priority_depts=None):

    df_new = df.copy()

    if priority_depts is None:
        priority_depts = df_new["Dept"].unique()[:5]

    mask = df_new["Dept"].isin(priority_depts)

    df_new.loc[mask, "allocated_inventory"] *= (1 + severity)

    return recompute_supply_metrics(df_new)