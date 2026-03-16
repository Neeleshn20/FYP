import streamlit as st
from core.data_engine import load_data
from core.scope_engine import get_store_selection, get_department_selection
from core.aggregation_engine import apply_aggregation
from core.phase1_metrics import compute_phase1
from core.graph_engine import render_graph
from core.render_engine import render_metrics_panel
from failure_modes.failure_registry import FAILURES
from core.phase2_report_engine import (
    render_failure_graph,
    render_metric_comparison,
    render_failure_summary,
    render_risk_escalation,
    render_loss_composition
)

st.set_page_config(layout="wide")
st.title("Detection and Analysis of Silent Decision Degradation in AI-Assisted Inventory Decision Systems")


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

# =========================================================
# TAB 2 — FAILURE INJECTION LABORATORY
# =========================================================

from failure_modes.failure_registry import FAILURES

with tab2:

    st.header("Phase 2 — Failure Injection Laboratory")

    st.markdown(
        """
        Inject disturbances into the baseline allocation policy
        and observe how the system degrades.
        """
    )

    # -----------------------------------------------------
    # FAILURE SELECTION
    # -----------------------------------------------------

    failure_name = st.selectbox(
        "Select Failure Mode",
        list(FAILURES.keys())
    )

    failure_config = FAILURES[failure_name]

    failure_function = failure_config["function"]
    param_name = failure_config.get("parameter", None)
    ui_config = failure_config.get("ui", None)

    param_value = None

    # -----------------------------------------------------
    # FAILURE PARAMETER CONTROL
    # -----------------------------------------------------

    if ui_config is not None:

        control_type = ui_config["type"]

        if control_type == "slider":

            param_value = st.slider(
                ui_config["label"],
                ui_config["min"],
                ui_config["max"],
                ui_config["default"],
                ui_config.get("step", 0.01)
            )

        elif control_type == "number_input":

            param_value = st.number_input(
                ui_config["label"],
                min_value=ui_config["min"],
                max_value=ui_config["max"],
                value=ui_config["default"]
            )

        elif control_type == "checkbox":

            param_value = st.checkbox(
                ui_config["label"],
                value=ui_config["default"]
            )

        elif control_type == "dropdown":

            param_value = st.selectbox(
                ui_config["label"],
                ui_config["options"]
            )

    else:

        st.info("This failure mode has no adjustable parameters.")

    # -----------------------------------------------------
    # BASELINE COMPUTATION
    # -----------------------------------------------------

    baseline_df, baseline_metrics = compute_phase1(
        filtered_view,
        margin,
        holding_cost
    )

    # -----------------------------------------------------
    # FAILURE INJECTION
    # -----------------------------------------------------

    temp = filtered_base.copy()

    if param_name is not None:

        temp = failure_function(
            temp,
            **{param_name: param_value}
        )

    else:

        temp = failure_function(temp)

    # apply aggregation after failure
    temp = apply_aggregation(temp, view_mode)

    failure_df, failure_metrics = compute_phase1(
        temp,
        margin,
        holding_cost
    )

    # -----------------------------------------------------
    # SYSTEM BEHAVIOR GRAPH
    # -----------------------------------------------------

    st.markdown("## Baseline vs Failure Behaviour")

    render_failure_graph(
        baseline_df,
        failure_df,
        show_actual,
        show_expected,
        show_allocated,
        show_loss,
        show_service
    )
    st.markdown("## Risk Escalation")
    render_risk_escalation(
        baseline_metrics,
        failure_metrics
    )
    # -----------------------------------------------------
    # METRIC COMPARISON
    # -----------------------------------------------------

    render_metric_comparison(
        baseline_metrics,
        failure_metrics
    )
    st.markdown("## Economic Loss Composition")

    render_loss_composition(
        baseline_df,
        failure_df
    )
    # -----------------------------------------------------
    # FAILURE INTERPRETATION
    # -----------------------------------------------------

    render_failure_summary(
        baseline_metrics,
        failure_metrics
    )