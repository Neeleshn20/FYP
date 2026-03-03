import streamlit as st
import pandas as pd


def render_phase2_comparison(baseline_metrics, failure_metrics):

    st.markdown("## 📊 Baseline vs Failure Comparison")

    comparison_data = []

    keys = [
        "fill_rate",
        "avg_service",
        "mape",
        "mean_volatility",
        "cv_allocation",
        "capital_efficiency",
        "loss_ratio",
        "total_loss"
    ]

    for k in keys:
        base = baseline_metrics[k]
        fail = failure_metrics[k]
        delta = fail - base

        comparison_data.append({
            "Metric": k,
            "Baseline": round(base, 4),
            "Failure": round(fail, 4),
            "Delta": round(delta, 4)
        })

    comparison_df = pd.DataFrame(comparison_data)

    st.dataframe(comparison_df, use_container_width=True)

    return comparison_df
def render_failure_insights(baseline_metrics, failure_metrics):

    st.markdown("## 🧠 Structural Impact Analysis")

    insights = []

    # Risk escalation
    risk_base = baseline_metrics["risk_score"]
    risk_fail = failure_metrics["risk_score"]

    if risk_fail > risk_base + 10:
        insights.append("Significant structural risk escalation detected.")
    elif risk_fail > risk_base:
        insights.append("Moderate risk increase observed.")
    else:
        insights.append("No meaningful risk escalation observed.")

    # Silent degradation
    if (
        abs(failure_metrics["avg_service"] - baseline_metrics["avg_service"]) < 0.01
        and risk_fail > risk_base + 5
    ):
        insights.append("⚠ Silent degradation detected: Service level stable but structural risk increased.")

    # Forecast instability
    if failure_metrics["mape"] > baseline_metrics["mape"]:
        insights.append("Forecast quality deteriorated under failure mode.")

    # Capital distortion
    if failure_metrics["capital_efficiency"] < baseline_metrics["capital_efficiency"]:
        insights.append("Capital efficiency degraded under disturbance.")

    for msg in insights:
        st.warning(msg)