def generate_summary(metrics):

    messages = []

    if metrics["MAPE"] < 0.15:
        messages.append("Forecast accuracy strong.")
    elif metrics["MAPE"] < 0.30:
        messages.append("Moderate forecast instability.")
    else:
        messages.append("High forecast instability detected.")

    if metrics["Allocation CV"] < 0.15:
        messages.append("Stable allocation behavior.")
    elif metrics["Allocation CV"] < 0.30:
        messages.append("Moderate allocation volatility.")
    else:
        messages.append("High allocation instability.")

    if metrics["Capital Efficiency"] >= 0.98:
        messages.append("Efficient capital usage.")
    elif metrics["Capital Efficiency"] >= 0.90:
        messages.append("Some capital inefficiency.")
    else:
        messages.append("Significant oversupply risk.")

    if metrics["Loss Ratio"] < 0.05:
        messages.append("Loss proportionally low.")
    elif metrics["Loss Ratio"] < 0.15:
        messages.append("Moderate economic degradation.")
    else:
        messages.append("Severe economic degradation.")

    return messages