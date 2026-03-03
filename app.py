import streamlit as st
from core.data_engine import load_data
from core.scope_engine import get_store_selection, get_department_selection
from core.aggregation_engine import apply_aggregation
from core.phase1_metrics import compute_phase1
from core.graph_engine import render_graph
from core.render_engine import render_metrics_panel
from failure_modes import signal_delay, demand_drift, holiday_amplification

st.set_page_config(layout="wide")
st.title("Decision System Laboratory")

df = load_data()

# Sidebar scope
selected_stores = get_store_selection(st, df)

view_mode = st.sidebar.radio(
    "Analysis Mode",
    ["Custom Selection", "Entire Store View"]
)

selected_depts, available_depts = get_department_selection(
    st, df, selected_stores, view_mode
)
with st.expander("🔎 Selected Store–Department Mapping"):
    st.write("Selected Stores:", selected_stores)
    st.write("Departments Available for Selection:", available_depts)
    st.write("Count of Available Departments:", len(available_depts))
    store_dept_map = (
    df.groupby("Store")["Dept"]
    .unique()
    .to_dict()
    )

    st.write("Departments in each selected store:")
    for store in selected_stores:
        st.write(f"Store {store} → {len(store_dept_map[store])} departments")

margin = st.sidebar.slider("Gross Margin (%)", 5, 50, 20)
holding_cost = st.sidebar.slider("Holding Cost (%)", 1, 10, 3)

show_actual = st.sidebar.checkbox("Show Actual Demand", True)
show_expected = st.sidebar.checkbox("Show Expected Demand", True)
show_allocated = st.sidebar.checkbox("Show Allocated Inventory", True)
show_loss = st.sidebar.checkbox("Show Weekly Loss", True)
show_service = st.sidebar.checkbox("Show Service Level", False)

filtered = df[
    (df["Store"].isin(selected_stores)) &
    (df["Dept"].isin(selected_depts))
].sort_values("Date")

filtered = apply_aggregation(filtered, view_mode)
# Raw filtered dataset (never aggregated)
filtered_base = df[
    (df["Store"].isin(selected_stores)) &
    (df["Dept"].isin(selected_depts))
].sort_values("Date")

if filtered_base.empty:
    st.warning("No data for selected filters.")
    st.stop()

# View-level dataset (aggregation depends on mode)
filtered_view = apply_aggregation(filtered_base.copy(), view_mode)
tab1, tab2 = st.tabs(["Phase 1 — Baseline", "Phase 2 — Failure Injection"])

with tab1:

    df_metrics, metrics = compute_phase1(filtered, margin, holding_cost)

    render_graph(
        st,
        df_metrics,
        show_actual,
        show_expected,
        show_allocated,
        show_loss,
        show_service
    )
    render_metrics_panel(metrics, df_metrics)
    st.write("Metrics computed — identical to original logic.")

with tab2:

    st.header("Failure Injection")

    failure = st.selectbox(
        "Select Failure Mode",
        ["Signal Delay", "Demand Drift", "Holiday Amplification"]
    )

    delay = st.slider("Signal Delay", 1, 8, 2)
    drift = st.slider("Demand Drift", 0.0, 0.5, 0.1)
    amp = st.slider("Holiday Amplification", 1.0, 3.0, 1.5)

    # Always start from raw filtered base
    temp = filtered_base.copy()

    if failure == "Signal Delay":
        temp = signal_delay.apply(temp, delay_weeks=delay)

    elif failure == "Demand Drift":
        temp = demand_drift.apply(temp, drift_rate=drift)

    elif failure == "Holiday Amplification":
        temp = holiday_amplification.apply(temp, drift_strength=amp)

    # Only AFTER injection
    temp = apply_aggregation(temp, view_mode)

    df_metrics, metrics = compute_phase1(temp, margin, holding_cost)

    render_graph(
        st,
        df_metrics,
        show_actual,
        show_expected,
        show_allocated,
        show_loss,
        show_service
    )
    baseline_df, baseline_metrics = compute_phase1(
        filtered_view, margin, holding_cost
    )

    failure_df, failure_metrics = compute_phase1(
        temp, margin, holding_cost
    )

    from core.phase2_report_engine import (
        render_phase2_comparison,
        render_failure_insights
    )

    comparison_df = render_phase2_comparison(
        baseline_metrics,
        failure_metrics
    )

    render_failure_insights(
        baseline_metrics,
        failure_metrics
    )