def apply(df, drift_rate=0.002):

    df_drift = df.copy()

    df_drift["time_index"] = (
        df_drift.groupby(["Store", "Dept"]).cumcount()
    )

    df_drift["drift_multiplier"] = (
        1 + drift_rate * df_drift["time_index"]
    )

    df_drift["expected_demand"] *= df_drift["drift_multiplier"]

    return df_drift