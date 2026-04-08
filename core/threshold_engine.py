def analyze_thresholds(results_df):

    threshold_results = []

    grouped = results_df.groupby("failure")

    for failure, group in grouped:

        group = group.sort_values("param")

        baseline = group[group["param"] == "BASELINE"]

        if baseline.empty:
            base_risk = group.iloc[0]["risk_score"]
            base_service = group.iloc[0]["avg_service"]
        else:
            base_risk = baseline.iloc[0]["risk_score"]
            base_service = baseline.iloc[0]["avg_service"]

        degradation_point = None
        critical_point = None
        silent_points = []

        for _, row in group.iterrows():

            risk_delta = row["risk_score"] - base_risk
            service_delta = row["avg_service"] - base_service

            # -------- degradation detection --------
            if degradation_point is None and risk_delta > 1:
                degradation_point = row["param"]

            # -------- critical detection --------
            if critical_point is None and risk_delta > 5:
                critical_point = row["param"]

            # -------- silent degradation --------
            if risk_delta > 1 and abs(service_delta) < 0.01:
                silent_points.append(row["param"])

        threshold_results.append({
            "failure": failure,
            "degradation_start": degradation_point,
            "critical_point": critical_point,
            "silent_zone": silent_points
        })

    return threshold_results