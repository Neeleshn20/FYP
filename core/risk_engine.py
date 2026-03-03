def compute_risk(metrics):

    forecast_risk = min(metrics["MAPE"] / 0.5, 1)
    volatility_risk = min(metrics["Allocation CV"] / 0.5, 1)
    capital_risk = min((1 - metrics["Capital Efficiency"]) / 0.5, 1)
    economic_risk = min(metrics["Loss Ratio"] / 0.3, 1)

    risk_score = (
        0.25 * forecast_risk +
        0.25 * volatility_risk +
        0.25 * capital_risk +
        0.25 * economic_risk
    ) * 100

    return risk_score