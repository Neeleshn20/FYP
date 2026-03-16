import pandas as pd
import streamlit as st
import plotly.graph_objects as go


# ----------------------------------------------------
# 1. BASELINE vs FAILURE GRAPH
# ----------------------------------------------------

def render_failure_graph(
        baseline_df,
        failure_df,
        show_actual,
        show_expected,
        show_allocated,
        show_loss,
        show_service):

    fig = go.Figure()

    # ---------------- ACTUAL DEMAND ----------------
    if show_actual:

        fig.add_trace(go.Scatter(
            x=baseline_df["Date"],
            y=baseline_df["Weekly_Sales"],
            name="Actual Demand (Baseline)",
            line=dict(color="cyan", width=3)
        ))

        fig.add_trace(go.Scatter(
            x=failure_df["Date"],
            y=failure_df["Weekly_Sales"],
            name="Actual Demand (Failure)",
            line=dict(color="blue", width=2, dash="dash")
        ))

    # ---------------- EXPECTED DEMAND ----------------
    if show_expected:

        fig.add_trace(go.Scatter(
            x=baseline_df["Date"],
            y=baseline_df["expected_demand"],
            name="Expected Demand (Baseline)",
            line=dict(color="orange", width=3)
        ))

        fig.add_trace(go.Scatter(
            x=failure_df["Date"],
            y=failure_df["expected_demand"],
            name="Expected Demand (Failure)",
            line=dict(color="yellow", width=2, dash="dash")
        ))

    # ---------------- ALLOCATION ----------------
    if show_allocated:

        fig.add_trace(go.Scatter(
            x=baseline_df["Date"],
            y=baseline_df["allocated_inventory"],
            name="Allocated Inventory (Baseline)",
            line=dict(color="yellow", width=3)
        ))

        fig.add_trace(go.Scatter(
            x=failure_df["Date"],
            y=failure_df["allocated_inventory"],
            name="Allocated Inventory (Failure)",
            line=dict(color="darkgreen", width=2, dash="dash")
        ))

    # ---------------- WEEKLY LOSS ----------------
    if show_loss:

        fig.add_trace(go.Bar(
            x=baseline_df["Date"],
            y=baseline_df["weekly_loss"],
            name="Weekly Loss (Baseline)",
            marker_color="magenta",
            opacity=0.35
        ))

        fig.add_trace(go.Bar(
            x=failure_df["Date"],
            y=failure_df["weekly_loss"],
            name="Weekly Loss (Failure)",
            marker_color="red",
            opacity=0.35
        ))

    # ---------------- SERVICE LEVEL ----------------
    if show_service:

        fig.add_trace(go.Scatter(
            x=baseline_df["Date"],
            y=baseline_df["service_level"],
            name="Service Level (Baseline)",
            line=dict(color="green", width=3),
            yaxis="y2"
        ))

        fig.add_trace(go.Scatter(
            x=failure_df["Date"],
            y=failure_df["service_level"],
            name="Service Level (Failure)",
            line=dict(color="gray", width=2, dash="dash"),
            yaxis="y2"
        ))

    # ---------------- LAYOUT ----------------
    fig.update_layout(
        template="plotly_dark",
        height=650,
        yaxis=dict(title="Units"),
        yaxis2=dict(
            title="Service Level",
            overlaying="y",
            side="right"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    st.plotly_chart(fig, use_container_width=True)
def render_metric_comparison(baseline_metrics, failure_metrics):

    # Only keep meaningful metrics
    important_metrics = [
        "total_sales",
        "total_allocated",
        "total_loss",
        "loss_ratio",
        "avg_weekly_loss",
        "mean_volatility",
        "avg_service",
        "mape",
        "fill_rate",
        "overstock_ratio",
        "capital_efficiency",
        "cv_allocation",
        "risk_score"
    ]

    rows = []

    for key in important_metrics:

        if key not in baseline_metrics or key not in failure_metrics:
            continue

        base = baseline_metrics[key]
        fail = failure_metrics[key]
        delta = fail - base

        rows.append({
            "Metric": key,
            "Baseline Model": round(base,4),
            "After Failure": round(fail,4),
            "Δ Change": round(delta,4)
        })

    df = pd.DataFrame(rows)

    # ---------------------------------
    # Color logic
    # ---------------------------------

    bad_metrics = [
        "mape",
        "mean_volatility",
        "cv_allocation",
        "overstock_ratio",
        "loss_ratio",
        "total_loss",
        "avg_weekly_loss",
        "risk_score"
    ]

    good_metrics = [
        "fill_rate",
        "avg_service",
        "capital_efficiency",
        "total_sales"
    ]

    def color_delta(row):

        metric = row["Metric"]
        delta = row["Δ Change"]

        if metric in bad_metrics:

            if delta > 0:
                return ["", "", "", "color:red"]
            else:
                return ["", "", "", "color:green"]

        if metric in good_metrics:

            if delta > 0:
                return ["", "", "", "color:green"]
            else:
                return ["", "", "", "color:red"]

        return ["", "", "", ""]

    styled = df.style.apply(color_delta, axis=1)

    st.markdown("### Metric Comparison")

    st.dataframe(styled, use_container_width=True)

# ----------------------------------------------------
# 3. IMPACT SUMMARY
# ----------------------------------------------------

def render_failure_summary(baseline_metrics, failure_metrics):

    st.markdown("### Failure Impact Summary")

    risk_delta = (
        failure_metrics["risk_score"]
        - baseline_metrics["risk_score"]
    )

    service_change = (
        failure_metrics["avg_service"]
        - baseline_metrics["avg_service"]
    )

    loss_delta = (
        failure_metrics["loss_ratio"]
        - baseline_metrics["loss_ratio"]
    )

    col1, col2, col3 = st.columns(3)

    # ------------------------------------------------
    # Structural Risk
    # ------------------------------------------------
    with col1:

        if risk_delta > 20:
            st.error("Structural Risk ↑↑  \nFailure strongly destabilizes the system.")

        elif risk_delta > 8:
            st.warning("Structural Risk ↑  \nModerate instability introduced.")

        elif risk_delta < -5:
            st.success("Structural Risk ↓  \nSystem stability slightly improved.")

        else:
            st.info("Structural Risk ~  \nMinimal structural change.")

    # ------------------------------------------------
    # Service Reliability
    # ------------------------------------------------
    with col2:

        if service_change < -0.02:
            st.error("Service Reliability ↓↓  \nCustomer demand satisfaction deteriorates.")

        elif service_change < -0.005:
            st.warning("Service Reliability ↓  \nSmall service degradation detected.")

        elif service_change > 0.01:
            st.success("Service Reliability ↑  \nDemand satisfaction improved.")

        else:
            st.info("Service Reliability ~  \nService level largely unchanged.")

    # ------------------------------------------------
    # Economic Impact
    # ------------------------------------------------
    with col3:

        if loss_delta > 0.05:
            st.error("Economic Loss ↑↑  \nFailure significantly increases economic exposure.")

        elif loss_delta > 0.01:
            st.warning("Economic Loss ↑  \nModerate cost increase observed.")

        elif loss_delta < -0.01:
            st.success("Economic Loss ↓  \nFailure unexpectedly reduces cost impact.")

        else:
            st.info("Economic Loss ~  \nLimited financial impact.")

    # ------------------------------------------------
    # Silent Degradation Detection
    # ------------------------------------------------

    if abs(service_change) < 0.01 and risk_delta > 8:

        st.warning(
            "⚠ Silent degradation detected: service level appears stable but system risk has increased."
        )
# ----------------------------------------------------
# 4. RISK ESCALATION CHART
# ----------------------------------------------------

def render_risk_escalation(baseline_metrics, failure_metrics):

    baseline_risk = baseline_metrics["risk_score"]
    failure_risk = failure_metrics["risk_score"]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=["Baseline System"],
        y=[baseline_risk],
        name="Baseline Risk",
        marker_color="green"
    ))

    fig.add_trace(go.Bar(
        x=["Failure System"],
        y=[failure_risk],
        name="Failure Risk",
        marker_color="red"
    ))

    fig.update_layout(
        template="plotly_dark",
        title="System Risk Escalation",
        yaxis_title="Risk Score",
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)


# ----------------------------------------------------
# 5. ECONOMIC LOSS COMPOSITION
# ----------------------------------------------------

def render_loss_composition(baseline_df, failure_df):

    # Baseline losses
    base_unmet = baseline_df["unmet_demand"].sum()
    base_overstock = baseline_df["overstock"].sum()

    # Failure losses
    fail_unmet = failure_df["unmet_demand"].sum()
    fail_overstock = failure_df["overstock"].sum()

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name="Lost Sales (Baseline)",
        x=["Baseline"],
        y=[base_unmet],
        marker_color="orange"
    ))

    fig.add_trace(go.Bar(
        name="Overstock (Baseline)",
        x=["Baseline"],
        y=[base_overstock],
        marker_color="blue"
    ))

    fig.add_trace(go.Bar(
        name="Lost Sales (Failure)",
        x=["Failure"],
        y=[fail_unmet],
        marker_color="darkorange"
    ))

    fig.add_trace(go.Bar(
        name="Overstock (Failure)",
        x=["Failure"],
        y=[fail_overstock],
        marker_color="darkblue"
    ))

    fig.update_layout(
        template="plotly_dark",
        title="Economic Loss Composition",
        yaxis_title="Units",
        height=450,
        barmode="stack"
    )

    st.plotly_chart(fig, use_container_width=True)