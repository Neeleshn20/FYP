def evaluate_all_failures(
    df_base,
    failures_dict,
    margin,
    holding_cost,
    view_mode,
    compute_fn,
    aggregation_fn,
    detection_fn
):

    results = []

    # Baseline
    base_df, base_metrics = compute_fn(df_base, margin, holding_cost)

    for name, failure_fn in failures_dict.items():

        print(f"\nRunning failure: {name}")

        temp = df_base.copy()

        try:
            temp = failure_fn(temp)

            print(f"{name} → SUCCESS")

        except Exception as e:
            print(f"{name} → FAILED: {e}")
            continue

        try:
            temp = aggregation_fn(temp, view_mode)
            _, failure_metrics = compute_fn(temp, margin, holding_cost)

        except Exception as e:
            print(f"{name} → METRIC FAIL: {e}")
            continue

        detection = detection_fn(base_metrics, failure_metrics)

        results.append({
            "failure": name,
            "risk_score": failure_metrics["risk_score"],
            "loss_ratio": failure_metrics["loss_ratio"],
            "service": failure_metrics["avg_service"],
            "severity": detection["severity"],
            "silent": detection["silent_degradation"]
        })

    return results