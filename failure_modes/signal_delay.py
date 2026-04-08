from failure_modes.utils import recompute_supply_metrics

def apply(df, delay_weeks=4):

    df_new = df.copy()

    df_new = df_new.sort_values(["Store", "Dept", "Date"])

    df_new["expected_demand"] = (
        df_new.groupby(["Store", "Dept"])["expected_demand"]
        .shift(delay_weeks)
    )

    df_new = df_new.dropna().reset_index(drop=True)

    df_new["allocated_inventory"] = df_new["expected_demand"]

    return recompute_supply_metrics(df_new)