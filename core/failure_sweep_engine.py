import pandas as pd

def run_failure_sweep(
    df,
    FAILURES,
    param_grid,
    margin,
    holding_cost,
    view_mode,
    compute_phase1,
    apply_aggregation
):

    results = []

    # ---------------- BASELINE ----------------
    base_df = apply_aggregation(df.copy(), view_mode)
    _, baseline_metrics = compute_phase1(base_df, margin, holding_cost)

    results.append({
        "failure": "BASELINE",
        "param": "None",
        **baseline_metrics
    })

    # ---------------- FAILURE SWEEP ----------------
    for failure_name, failure_fn in FAILURES.items():

        if failure_name not in param_grid:
            continue

        param_name = param_grid[failure_name]["param"]
        values = param_grid[failure_name]["values"]

        for val in values:

            temp = df.copy()

            try:
                temp = failure_fn(temp, **{param_name: val})
            except Exception as e:
                continue

            temp = apply_aggregation(temp, view_mode)

            _, metrics = compute_phase1(temp, margin, holding_cost)

            results.append({
                "failure": failure_name,
                "param": ", ".join([f"{k}={v}" for k, v in param_grid.items()]),
                "risk_score": metrics["risk_score"],
                "loss_ratio": metrics["loss_ratio"],
                "avg_service": metrics["avg_service"],

                # 🔥 ADD THESE
                "mean_volatility": metrics["mean_volatility"],
                "cv_allocation": metrics["cv_allocation"],
                "overstock_ratio": metrics["overstock_ratio"],
                "capital_efficiency": metrics["capital_efficiency"],
                "mape": metrics["mape"]
            })

    return pd.DataFrame(results)