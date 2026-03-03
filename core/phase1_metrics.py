import numpy as np

def compute_phase1(filtered, margin, holding_cost):

    df = filtered.copy()

    df["lost_sales_cost"] = df["unmet_demand"] * (margin / 100)
    df["holding_cost"] = df["overstock"] * (holding_cost / 100)
    df["weekly_loss"] = df["lost_sales_cost"] + df["holding_cost"]
    df["cumulative_loss"] = df["weekly_loss"].cumsum()

    total_sales = df["Weekly_Sales"].sum()
    total_allocated = df["allocated_inventory"].sum()
    total_loss = df["cumulative_loss"].iloc[-1]

    loss_ratio = total_loss / total_sales if total_sales != 0 else 0
    avg_weekly_loss = df["weekly_loss"].mean()

    df["allocation_volatility"] = df["allocated_inventory"].diff().abs()
    mean_volatility = df["allocation_volatility"].mean()
    avg_service = df["service_level"].mean()

    df["forecast_error"] = df["Weekly_Sales"] - df["expected_demand"]
    df["abs_forecast_error"] = df["forecast_error"].abs()

    mape = (
        (df["abs_forecast_error"] / df["Weekly_Sales"])
        .replace([np.inf, -np.inf], np.nan)
        .dropna()
        .mean()
    )

    fill_rate = 1 - (
        df["unmet_demand"].sum() /
        df["Weekly_Sales"].sum()
    )

    overstock_ratio = (
        df["overstock"].sum() /
        df["allocated_inventory"].sum()
    )

    capital_efficiency = (
        df["Weekly_Sales"].sum() /
        df["allocated_inventory"].sum()
    )

    cv_allocation = (
        df["allocated_inventory"].std() /
        df["allocated_inventory"].mean()
    )

    # -------------------------
    # RISK SCORE COMPUTATION
    # -------------------------

    forecast_risk = min(mape / 0.5, 1)
    volatility_risk = min(cv_allocation / 0.5, 1)
    capital_risk = min((1 - capital_efficiency) / 0.5, 1)
    economic_risk = min(loss_ratio / 0.3, 1)

    risk_score = (
        0.25 * forecast_risk +
        0.25 * volatility_risk +
        0.25 * capital_risk +
        0.25 * economic_risk
    ) * 100

    return df, locals()