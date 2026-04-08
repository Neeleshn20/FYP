import numpy as np
from failure_modes.utils import recompute_supply_metrics

def apply(df, severity=0.3, dept_count=5):

    df_new = df.copy()

    coupled = df_new["Dept"].unique()[:dept_count]

    mask = df_new["Dept"].isin(coupled)

    oscillation = np.sin(np.linspace(0, 10, mask.sum()))

    df_new.loc[mask, "Weekly_Sales"] *= (1 + severity * oscillation)

    return recompute_supply_metrics(df_new)