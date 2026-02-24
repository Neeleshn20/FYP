import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("Phase 1 Decision Stress Laboratory")

# -------------------------
# LOAD DATA
# -------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("outputs/phase1_decisions.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

# -------------------------
# SIDEBAR CONTROLS
# -------------------------

st.sidebar.header("Control Panel")

# -------- STORE SELECTION --------

all_stores = sorted(df["Store"].unique())

select_all_stores = st.sidebar.checkbox("Select All Stores", value=True)

if select_all_stores:
    selected_stores = all_stores
else:
    selected_stores = st.sidebar.multiselect(
        "Select Store(s)",
        options=all_stores,
        default=[all_stores[0]]
    )

if not selected_stores:
    st.warning("Please select at least one store.")
    st.stop()

# -------- VIEW MODE --------

view_mode = st.sidebar.radio(
    "Analysis Mode",
    ["Custom Selection", "Entire Store View"]
)

# -------- DEPARTMENT LOGIC --------

available_depts = sorted(
    df[df["Store"].isin(selected_stores)]["Dept"].unique()
)

if view_mode == "Entire Store View":
    selected_depts = available_depts
    st.sidebar.info("All departments for selected store(s) included.")
else:
    select_all_depts = st.sidebar.checkbox("Select All Departments", value=True)

    if select_all_depts:
        selected_depts = available_depts
    else:
        selected_depts = st.sidebar.multiselect(
            "Select Department(s)",
            options=available_depts,
            default=[available_depts[0]] if available_depts else []
        )

if not selected_depts:
    st.warning("No departments available for selection.")
    st.stop()

# -------- GRAPH LAYERS --------

st.sidebar.subheader("Graph Layers")

show_actual = st.sidebar.checkbox("Show Actual Demand", value=True)
show_expected = st.sidebar.checkbox("Show Expected Demand", value=True)
show_allocated = st.sidebar.checkbox("Show Allocated Inventory", value=True)
show_loss = st.sidebar.checkbox("Show Weekly Loss", value=True)
show_service = st.sidebar.checkbox("Show Service Level", value=False)

# -------- ECONOMIC PARAMETERS --------

margin = st.sidebar.slider("Gross Margin (%)", 5, 50, 20)
holding_cost = st.sidebar.slider("Holding Cost (%)", 1, 10, 3)

# -------------------------
# FILTER DATA
# -------------------------

filtered = df[
    (df["Store"].isin(selected_stores)) &
    (df["Dept"].isin(selected_depts))
].sort_values("Date")

if filtered.empty:
    st.warning("No data for selected filters.")
    st.stop()

# -------------------------
# AGGREGATION FOR ENTIRE STORE VIEW
# -------------------------

if view_mode == "Entire Store View":

    aggregated = (
        filtered.groupby("Date")
        .agg({
            "Weekly_Sales": "sum",
            "expected_demand": "sum",
            "allocated_inventory": "sum",
            "unmet_demand": "sum",
            "overstock": "sum"
        })
        .reset_index()
    )

    # Correct service level calculation at aggregate level
    aggregated["service_level"] = 1 - (
        aggregated["unmet_demand"] / aggregated["Weekly_Sales"]
    )

    filtered = aggregated

# -------------------------
# ECONOMIC LOSS ENGINE
# -------------------------

filtered["lost_sales_cost"] = (
    filtered["unmet_demand"] * (margin / 100)
)

filtered["holding_cost"] = (
    filtered["overstock"] * (holding_cost / 100)
)

filtered["weekly_loss"] = (
    filtered["lost_sales_cost"] + filtered["holding_cost"]
)

filtered["cumulative_loss"] = filtered["weekly_loss"].cumsum()

# -------------------------
# VOLATILITY METRIC
# -------------------------

filtered["allocation_volatility"] = (
    filtered["allocated_inventory"].diff().abs()
)

mean_volatility = filtered["allocation_volatility"].mean()
avg_service = filtered["service_level"].mean()


# -------------------------
# ADDITIONAL METRICS
# -------------------------

# Forecast Error
filtered["forecast_error"] = (
    filtered["Weekly_Sales"] - filtered["expected_demand"]
)

filtered["abs_forecast_error"] = filtered["forecast_error"].abs()

mape = (
    (filtered["abs_forecast_error"] / filtered["Weekly_Sales"])
    .replace([np.inf, -np.inf], np.nan)
    .dropna()
    .mean()
)

# Fill Rate (Demand Weighted Service)
fill_rate = 1 - (
    filtered["unmet_demand"].sum() /
    filtered["Weekly_Sales"].sum()
)

# Overstock Ratio
overstock_ratio = (
    filtered["overstock"].sum() /
    filtered["allocated_inventory"].sum()
)

# Capital Efficiency
capital_efficiency = (
    filtered["Weekly_Sales"].sum() /
    filtered["allocated_inventory"].sum()
)

# Allocation Coefficient of Variation
cv_allocation = (
    filtered["allocated_inventory"].std() /
    filtered["allocated_inventory"].mean()
)

# -------------------------
# MAIN GRAPH
# -------------------------

fig = go.Figure()

if show_actual:
    fig.add_trace(go.Scatter(
        x=filtered["Date"],
        y=filtered["Weekly_Sales"],
        name="Actual Demand",
        mode="lines"
    ))

if show_expected:
    fig.add_trace(go.Scatter(
        x=filtered["Date"],
        y=filtered["expected_demand"],
        name="Expected Demand",
        mode="lines",
        line=dict(dash="dash")
    ))

if show_allocated:
    fig.add_trace(go.Scatter(
        x=filtered["Date"],
        y=filtered["allocated_inventory"],
        name="Allocated Inventory",
        mode="lines",
        line=dict(dash="dash")
    ))

if show_loss:
    fig.add_trace(go.Bar(
        x=filtered["Date"],
        y=filtered["weekly_loss"],
        name="Weekly Economic Loss",
        yaxis="y2",
        opacity=0.4
    ))

if show_service:
    fig.add_trace(go.Scatter(
        x=filtered["Date"],
        y=filtered["service_level"],
        name="Service Level",
        mode="lines",
        yaxis="y2"
    ))

fig.update_layout(
    template="plotly_dark",
    height=600,
    yaxis=dict(title="Units"),
    yaxis2=dict(
        title="Loss / Service Level",
        overlaying="y",
        side="right"
    )
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------
# METRICS PANEL
# -------------------------

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
    st.metric("Cumulative Economic Loss", f"{filtered['cumulative_loss'].iloc[-1]:,.2f}")
    st.caption("Total cost from unmet demand and overstock under current cost assumptions.")

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
if filtered["cumulative_loss"].iloc[-1] > 0:
    loss_ratio = filtered["cumulative_loss"].iloc[-1] / filtered["Weekly_Sales"].sum()
    
    if loss_ratio < 0.05:
        summary_messages.append("Economic loss remains proportionally low relative to total sales.")
    elif loss_ratio < 0.15:
        summary_messages.append("Noticeable economic loss relative to sales volume.")
    else:
        summary_messages.append("Severe economic degradation relative to realized demand.")

# Render Summary Box
with st.container():
    st.info("\n\n".join(summary_messages))


# -------------------------
# SYSTEM RISK SCORE
# -------------------------

# Normalize Forecast Risk
forecast_risk = min(mape / 0.5, 1)  # assuming 50% MAPE is extreme

# Normalize Volatility Risk
volatility_risk = min(cv_allocation / 0.5, 1)

# Normalize Capital Inefficiency Risk
capital_risk = min((1 - capital_efficiency) / 0.5, 1)

# Normalize Economic Loss Risk
loss_ratio = filtered["cumulative_loss"].iloc[-1] / filtered["Weekly_Sales"].sum()
economic_risk = min(loss_ratio / 0.3, 1)  # 30% loss ratio is severe

# Weighted Composite Risk Score
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