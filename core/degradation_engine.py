def detect_degradation(baseline, current):

    risk_change = current["risk_score"] - baseline["risk_score"]
    service_change = current["avg_service"] - baseline["avg_service"]
    loss_change = current["loss_ratio"] - baseline["loss_ratio"]

    silent = False
    degradation=False
    # -------- Silent degradation --------
    if risk_change > 0.5 and abs(service_change) < 0.01:
        silent = True
    if risk_change > 0.5:
        degradation = True
    # -------- Severity --------
    if risk_change < 0.2 and loss_change < 0.002:
        status = "STABLE"
    elif risk_change < 1:
        status = "DEGRADED"
    else:
        status = "CRITICAL"

    return {
        "degradation": degradation,
        "severity": status,
        "silent": silent,
        "risk_change": risk_change,
        "service_change": service_change,
        "loss_change": loss_change
    }