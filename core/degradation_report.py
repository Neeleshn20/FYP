import streamlit as st

def render_degradation_report(detection_result):

    st.markdown("## Degradation Detection")

    if detection_result["severity"] == "Severe":
        st.error("Severe system degradation detected.")

    elif detection_result["severity"] == "Moderate":
        st.warning("Moderate degradation observed.")

    elif detection_result["severity"] == "Mild":
        st.info("Mild degradation present.")

    else:
        st.success("No meaningful degradation detected.")

    # Silent degradation
    if detection_result["silent_degradation"]:
        st.warning(
            "⚠ Silent degradation detected — system appears stable but risk has increased."
        )

    # Quantitative summary
    st.markdown("### Key Changes")

    st.write(f"Risk Change: {detection_result['risk_delta']:.2f}")
    st.write(f"Service Change: {detection_result['service_delta']:.4f}")
    st.write(f"Loss Change: {detection_result['loss_delta']:.4f}")