import streamlit as st
import pandas as pd
# ---------------- CORE IMPORTS ----------------
from core.data_loader import load_data
from core.scope_engine import get_store_selection, get_department_selection
from core.aggregation_engine import apply_aggregation
from core.phase1_metrics import compute_phase1
from core.graph_engine import render_graph
from core.render_engine import render_metrics_panel
from core.param_config import PARAM_GRID
from core.failure_sweep_engine import run_failure_sweep
# ---------------- FAILURE + REPORTING ----------------
from failure_modes.failure_registry import FAILURES

from core.phase2_report_engine import (
    render_failure_graph,
    render_metric_comparison,
    render_failure_summary,
    render_risk_escalation,
    render_loss_composition
)

from core.phase3_engine import evaluate_all_failures
from core.phase3_renderer import render_phase3_dashboard
from core.degradation_engine import detect_degradation
from core.threshold_engine import analyze_thresholds
from core.behavioral_detection import detect_behavioral_instability
from core.structural_detection import detect_structural_failure
# ---------------- APP CONFIG ----------------
st.set_page_config(layout="wide")
st.title("Detection and Analysis of Silent Decision Degradation in AI-Assisted Inventory Decision Systems")

# ---------------- LOAD DATA ----------------
df = load_data()

# ---------------- SIDEBAR: SCOPE ----------------
selected_stores = get_store_selection(st, df)

view_mode = st.sidebar.radio(
    "Analysis Mode",
    ["Custom Selection", "Entire Store View"]
)

selected_depts, available_depts = get_department_selection(
    st, df, selected_stores, view_mode
)

# ---------------- DEBUG PANEL ----------------
with st.expander("🔎 Selected Store–Department Mapping"):
    st.write("Selected Stores:", selected_stores)
    st.write("Departments Available:", available_depts)
    st.write("Count:", len(available_depts))

    store_dept_map = df.groupby("Store")["Dept"].unique().to_dict()

    for store in selected_stores:
        st.write(f"Store {store} → {len(store_dept_map[store])} departments")

# ---------------- ECON PARAMS ----------------
margin = st.sidebar.slider("Gross Margin (%)", 5, 50, 20)
holding_cost = st.sidebar.slider("Holding Cost (%)", 1, 10, 3)

# ---------------- GRAPH LAYERS ----------------
show_actual = st.sidebar.checkbox("Show Actual Demand", True)
show_expected = st.sidebar.checkbox("Show Expected Demand", True)
show_allocated = st.sidebar.checkbox("Show Allocated Inventory", True)
show_loss = st.sidebar.checkbox("Show Weekly Loss", True)
show_service = st.sidebar.checkbox("Show Service Level", False)

# ---------------- FILTER DATA ----------------
filtered_base = df[
    (df["Store"].isin(selected_stores)) &
    (df["Dept"].isin(selected_depts))
].sort_values("Date")

if filtered_base.empty:
    st.warning("No data for selected filters.")
    st.stop()

filtered_view = apply_aggregation(filtered_base.copy(), view_mode)

# ---------------- TABS ----------------
tab1, tab2, tab3 = st.tabs([
    "Phase 1 — Baseline",
    "Phase 2 — Failure Lab",
    "Phase 3 — System Diagnosis"
])

# =========================================================
# TAB 1 — BASELINE
# =========================================================
with tab1:

    df_metrics, metrics = compute_phase1(filtered_view, margin, holding_cost)

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

# =========================================================
# TAB 2 — FAILURE LAB
# =========================================================
with tab2:

    st.header("Phase 2 — Failure Injection Laboratory")

    failure_name = st.selectbox(
        "Select Failure Mode",
        list(FAILURES.keys())
    )

    failure_config = FAILURES[failure_name]

    # ---------------- FIX: HANDLE BOTH DESIGNS ----------------
    if isinstance(failure_config, dict):
        failure_function = failure_config["function"]
        param_name = failure_config.get("parameter", None)
        ui_config = failure_config.get("ui", None)
    else:
        # simple function-only registry
        failure_function = failure_config
        param_name = None
        ui_config = None

    param_value = None

    # ---------------- PARAM CONTROL ----------------
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
        st.info("No adjustable parameters for this failure.")

    # ---------------- BASELINE ----------------
    baseline_df, baseline_metrics = compute_phase1(
        filtered_view,
        margin,
        holding_cost
    )

    # ---------------- APPLY FAILURE ----------------
    temp = filtered_base.copy()

    try:
        if param_name is not None:
            temp = failure_function(temp, **{param_name: param_value})
        else:
            temp = failure_function(temp)
    except Exception as e:
        st.error(f"Failure execution error: {e}")
        st.stop()

    temp = apply_aggregation(temp, view_mode)

    failure_df, failure_metrics = compute_phase1(
        temp,
        margin,
        holding_cost
    )

    # ---------------- VISUALIZATION ----------------
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
    render_risk_escalation(baseline_metrics, failure_metrics)

    render_metric_comparison(baseline_metrics, failure_metrics)

    st.markdown("## Economic Loss Composition")
    render_loss_composition(baseline_df, failure_df)

    render_failure_summary(baseline_metrics, failure_metrics)

# =========================================================
# PHASE 3 — SYSTEM DIAGNOSIS
# =========================================================

with tab3:

    # -----------------------------------------------------
    # SYSTEM SUMMARY
    # -----------------------------------------------------

    st.markdown("## 🧠 System Risk Overview")

    baseline_metrics = compute_phase1(
        apply_aggregation(filtered_base, view_mode),
        margin,
        holding_cost
    )[1]
        # Run full sweep
    results_df = run_failure_sweep(
        filtered_base,
        FAILURES,
        PARAM_GRID,
        margin,
        holding_cost,
        view_mode,
        compute_phase1,
        apply_aggregation
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Baseline Risk", f"{baseline_metrics['risk_score']:.2f}")

    with col2:
        st.metric("Max Risk Observed", f"{results_df['risk_score'].max():.2f}")

    with col3:
        st.metric(
            "Degradation Cases",
            int((results_df["risk_score"] > baseline_metrics["risk_score"]).sum())
    )


    # -----------------------------------------------------
    # CLEAN TABLE FOR DISPLAY
    # -----------------------------------------------------

    display_df = results_df[[
        "failure",
        "param",
        "risk_score",
        "loss_ratio",
        "avg_service"
    ]].copy()

    display_df = display_df.rename(columns={
            "failure": "Failure Mode",
            "param": "Parameter",
            "risk_score": "Risk Score",
            "loss_ratio": "Loss Ratio",
            "avg_service": "Service Level"
        })
        # CLEAN PARAMETER COLUMN (CRITICAL FIX)
    display_df["Parameter"] = display_df["Parameter"].astype(str)
    display_df["Parameter"] = display_df["Parameter"].apply(
        lambda x: x.split("=")[-1] if "=" in x else x
    )
    st.subheader("📊 Failure Experiment Table")

    st.dataframe(
        display_df.sort_values(["Failure Mode", "Parameter"]),
        use_container_width=True,
        height=400
    )

    # -----------------------------------------------------
    # ADD DEGRADATION FLAGS
    # -----------------------------------------------------

    st.subheader("🚨 Degradation Classification")

    baseline_metrics = compute_phase1(
        apply_aggregation(filtered_base, view_mode),
        margin,
        holding_cost
    )[1]



    classification_rows = []

    for _, row in results_df.iterrows():

        current = {
            "risk_score": row["risk_score"],
            "loss_ratio": row["loss_ratio"],
            "avg_service": row["avg_service"],

            # 🔥 ADD THESE (CRITICAL)
            "mean_volatility": row["mean_volatility"],
            "cv_allocation": row["cv_allocation"],
            "overstock_ratio": row["overstock_ratio"],
            "capital_efficiency": row["capital_efficiency"],
            "mape": row["mape"]
        }

        status = detect_degradation(baseline_metrics, current)
        behavior_flags = detect_behavioral_instability(current)
        structural_flags = detect_structural_failure(current)

        classification_rows.append({
            "Failure": row["failure"],
            "Parameter": row["param"],
            "Risk Score": round(row["risk_score"], 2),
            "Degradation": status["degradation"],
            "Silent": status["silent"],
            "Behavioral Issues": ", ".join(behavior_flags),
            "Structural Issues": ", ".join(structural_flags)
        })

    classification_df = pd.DataFrame(classification_rows)
    # CLEAN PARAM COLUMN HERE ALSO
    classification_df["Parameter"] = classification_df["Parameter"].astype(str)
    classification_df["Parameter"] = classification_df["Parameter"].apply(
        lambda x: x.split("=")[-1] if "=" in x else x
    )
    st.dataframe(classification_df, use_container_width=True)

    # -----------------------------------------------------
    # THRESHOLD ANALYSIS (your existing logic)
    # -----------------------------------------------------

    thresholds = analyze_thresholds(results_df)

    st.subheader("🚨 Failure Threshold Analysis")

    for t in thresholds:

        st.markdown(f"### {t['failure']}")

        st.write(f"🟡 Degradation starts at: {t['degradation_start']}")
        st.write(f"🔴 Critical point at: {t['critical_point']}")

        if t["silent_zone"]:
            st.warning(f"⚠ Silent degradation: {t['silent_zone']}")
        else:
            st.success("No silent degradation")

    # -----------------------------------------------------
    # SILENT DEGRADATION SUMMARY
    # -----------------------------------------------------

    st.subheader("⚠ Silent Degradation Zones")

    silent_df = classification_df[classification_df["Silent"] == True]

    if silent_df.empty:
        st.success("No silent degradation detected")
    else:
        grouped = silent_df.groupby("Failure")["Parameter"].apply(list)

        for failure, params in grouped.items():
            st.warning(f"{failure} → {list(set(params))}")

    # -----------------------------------------------------
    # TOP FAILURES
    # -----------------------------------------------------

    

    st.markdown("## 🔥 Most Critical Failures")

    top_failures = (
        results_df.sort_values("risk_score", ascending=False)
        .groupby("failure")
        .first()
        .reset_index()
        .head(5)
    )

    for _, row in top_failures.iterrows():
        st.error(f"{row['failure']} → Risk Score: {row['risk_score']:.2f}")