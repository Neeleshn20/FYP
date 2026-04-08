def identify_best_failure(df):

    df = df[df["failure"] != "BASELINE"]

    # Worst by risk
    worst_risk = df.loc[df["risk_score"].idxmax()]

    # Worst by loss
    worst_loss = df.loc[df["loss_ratio"].idxmax()]

    # Silent degradation candidates
    silent_df = df[
        (df["risk_score"] > df["risk_score"].mean()) &
        (abs(df["avg_service_level"] - df["avg_service_level"].mean()) < 0.01)
    ]

    silent_failure = None
    if not silent_df.empty:
        silent_failure = silent_df.loc[silent_df["risk_score"].idxmax()]

    return worst_risk, worst_loss, silent_failure