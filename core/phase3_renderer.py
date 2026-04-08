import pandas as pd
import streamlit as st
import plotly.express as px


def render_phase3_dashboard(results):

    df = pd.DataFrame(results)

    st.markdown("## Failure Risk Landscape")

    # -------------------------
    # TABLE
    # -------------------------
    st.dataframe(df, use_container_width=True)

    # -------------------------
    # RISK BAR CHART
    # -------------------------
    fig = px.bar(
        df,
        x="failure",
        y="risk_score",
        color="severity",
        title="Risk Score Across Failures"
    )

    st.plotly_chart(fig, use_container_width=True)

    # -------------------------
    # SILENT FAILURES
    # -------------------------
    silent_df = df[df["silent"] == True]

    st.markdown("## Silent Degradation Risks")

    if silent_df.empty:
        st.success("No silent failures detected")
    else:
        st.warning("Hidden failures detected:")
        st.dataframe(silent_df)

    # -------------------------
    # TOP FAILURES
    # -------------------------
    top = df.sort_values("risk_score", ascending=False).head(3)

    st.markdown("## Top Risk Failures")

    for _, row in top.iterrows():
        st.write(f"{row['failure']} → Risk: {row['risk_score']:.2f}")


    if not results:
        st.error("No valid failure results generated.")
        st.stop()

    df = pd.DataFrame(results)

    if df.empty or "failure" not in df.columns:
        st.error("Phase 3 data invalid. Check failure execution.")
        st.stop()