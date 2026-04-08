from failure_modes.utils import recompute_supply_metrics

def apply(df, drift_rate=0.002):

    df_new = df.copy()

    df_new["time_index"] = (
        df_new.groupby(["Store", "Dept"]).cumcount()
    )

    df_new["expected_demand"] *= (1 + drift_rate * df_new["time_index"])

    df_new["allocated_inventory"] = df_new["expected_demand"]

    return recompute_supply_metrics(df_new)