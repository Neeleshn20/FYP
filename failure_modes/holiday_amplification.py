import numpy as np
np.random.seed(42)
def apply(df, drift_strength=0.3):

    df_h = df.copy()

    noise = np.random.normal(
        0,
        drift_strength,
        size=len(df_h)
    )

    holiday_mask = df_h["IsHoliday"] == True

    df_h.loc[holiday_mask, "expected_demand"] *= (
        1 + noise[holiday_mask]
    )

    return df_h
