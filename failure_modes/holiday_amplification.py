import numpy as np
from failure_modes.utils import recompute_supply_metrics

def apply(df, drift_strength=0.3):

    df_new = df.copy()

    noise = np.random.normal(0, drift_strength, len(df_new))

    mask = df_new["IsHoliday"]

    df_new.loc[mask, "expected_demand"] *= (1 + noise[mask])

    df_new["allocated_inventory"] = df_new["expected_demand"]

    return recompute_supply_metrics(df_new)
