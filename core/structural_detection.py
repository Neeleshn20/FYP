def detect_structural_failure(metrics):

    flags = []

    # Concentration / imbalance
    if metrics["overstock_ratio"] > 0.15:
        flags.append("Inventory Concentration Risk")

    # Capital distortion
    if metrics["capital_efficiency"] < 0.9:
        flags.append("Capital Misallocation")

    # Regime shift signal
    if metrics["mape"] > 0.15:
        flags.append("Demand Regime Shift")

    return flags