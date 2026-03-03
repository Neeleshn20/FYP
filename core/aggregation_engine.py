def apply_aggregation(filtered, view_mode):

    if view_mode == "Entire Store View":

        aggregated = (
            filtered.groupby("Date")
            .agg({
                "Weekly_Sales": "sum",
                "expected_demand": "sum",
                "allocated_inventory": "sum",
                "unmet_demand": "sum",
                "overstock": "sum"
            })
            .reset_index()
        )

        aggregated["service_level"] = 1 - (
            aggregated["unmet_demand"] / aggregated["Weekly_Sales"]
        )

        return aggregated

    return filtered