import streamlit as st

def render_metrics_panel(metrics, df):

    fill_rate = metrics["fill_rate"]
    avg_service = metrics["avg_service"]
    mape = metrics["mape"]
    mean_volatility = metrics["mean_volatility"]
    cv_allocation = metrics["cv_allocation"]
    overstock_ratio = metrics["overstock_ratio"]
    capital_efficiency = metrics["capital_efficiency"]
    total_sales = metrics["total_sales"]
    total_loss = metrics["total_loss"]
    loss_ratio = metrics["loss_ratio"]
    avg_weekly_loss = metrics["avg_weekly_loss"]
    risk_score = metrics["risk_score"]
    # -------------------------
    # DECISION HEALTH PANEL
    # -------------------------

    st.markdown("## Decision Health Panel")

    # Row 1 — Performance & Forecast Quality
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Fill Rate (Weighted)", f"{fill_rate:.3f}")
        st.caption("Demand-weighted fraction of demand satisfied. More honest than averaging service level.")

    with col2:
        st.metric("Average Service Level", f"{avg_service:.3f}")
        st.caption("Mean of weekly service levels. Can mask large spikes in unmet demand.")

    with col3:
        st.metric("Forecast MAPE", f"{mape:.3f}")
        st.caption("Mean Absolute Percentage Error of forecast. Higher values indicate unstable demand prediction.")

    # Row 2 — Stability & Allocation Behavior
    col4, col5, col6 = st.columns(3)

    with col4:
        st.metric("Mean Allocation Volatility", f"{mean_volatility:,.2f}")
        st.caption("Average week-to-week change in allocation. High values imply unstable decision policy.")

    with col5:
        st.metric("Allocation CV", f"{cv_allocation:.3f}")
        st.caption("Coefficient of variation of allocation. Normalized instability measure across time.")

    with col6:
        st.metric("Overstock Ratio", f"{overstock_ratio:.3f}")
        st.caption("Fraction of allocated inventory that became excess. Indicates trapped capital.")

    # Row 3 — Capital & Economic Impact
    col7, col8 = st.columns(2)

    with col7:
        st.metric("Capital Efficiency", f"{capital_efficiency:.3f}")
        st.caption("Sales-to-allocation ratio. Values below 1 indicate systemic oversupply.")

    with col8:
        st.metric("Cumulative Economic Loss", f"{total_loss:,.2f}")
        st.caption("Total cost from unmet demand and overstock under current cost assumptions.")

    # Row 4 — Scale & Exposure
    col9, col10, col11 = st.columns(3)

    with col9:
        st.metric("Total Sales", f"{total_sales:,.2f}")
        st.caption("Aggregate realized demand across selected filters.")

    with col10:
        st.metric("Average Weekly Loss", f"{avg_weekly_loss:,.2f}")
        st.caption("Mean weekly economic damage over selected period.")

    with col11:
        st.metric("Loss Ratio", f"{loss_ratio:.3f}")
        st.caption("Proportion of total sales lost due to unmet demand and overstock.")

    # -------------------------
    # SYSTEM HEALTH SUMMARY
    # -------------------------

    st.markdown("## System Health Summary")

    summary_messages = []

    # Forecast Quality
    if mape < 0.15:
        summary_messages.append("Forecast accuracy is strong. Allocation errors are likely policy-driven rather than demand-driven.")
    elif mape < 0.30:
        summary_messages.append("Forecast accuracy is moderate. Some instability may be demand uncertainty.")
    else:
        summary_messages.append("High forecast error detected. Demand unpredictability is stressing the allocation policy.")

    # Stability
    if cv_allocation < 0.15:
        summary_messages.append("Allocation policy appears stable over time.")
    elif cv_allocation < 0.30:
        summary_messages.append("Moderate allocation volatility observed. Policy adjustments may be reactive.")
    else:
        summary_messages.append("High allocation instability detected. Decision policy may be oscillatory or overreacting.")

    # Capital Efficiency
    if capital_efficiency >= 0.98:
        summary_messages.append("Capital utilization is efficient with minimal oversupply.")
    elif capital_efficiency >= 0.90:
        summary_messages.append("Some capital inefficiency present due to oversupply.")
    else:
        summary_messages.append("Significant capital inefficiency detected. System is allocating beyond realized demand.")

    # Economic Loss Scale
    if total_loss > 0:
        if loss_ratio < 0.05:
            summary_messages.append("Economic loss remains proportionally low relative to total sales.")
        elif loss_ratio < 0.15:
            summary_messages.append("Noticeable economic loss relative to sales volume.")
        else:
            summary_messages.append("Severe economic degradation relative to realized demand.")

    with st.container():
        st.info("\n\n".join(summary_messages))

    # -------------------------
    # SYSTEM RISK SCORE
    # -------------------------

    forecast_risk = min(mape / 0.5, 1)
    volatility_risk = min(cv_allocation / 0.5, 1)
    capital_risk = min((1 - capital_efficiency) / 0.5, 1)
    economic_risk = min(loss_ratio / 0.3, 1)

    risk_score = (
        0.25 * forecast_risk +
        0.25 * volatility_risk +
        0.25 * capital_risk +
        0.25 * economic_risk
    ) * 100

    st.markdown("## System Risk Score")

    if risk_score < 30:
        st.success(f"Low Risk Environment — Score: {risk_score:.1f}/100")
    elif risk_score < 60:
        st.warning(f"Moderate System Risk — Score: {risk_score:.1f}/100")
    else:
        st.error(f"High Structural Risk Detected — Score: {risk_score:.1f}/100")

    st.caption("Composite risk based on forecast error, allocation volatility, capital inefficiency, and economic loss exposure.")