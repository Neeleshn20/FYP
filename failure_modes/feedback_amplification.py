def apply(df, feedback_strength=0.4):

    df_new = df.copy()

    df_new = df_new.sort_values(["Store","Dept","Date"])

    df_new["prev_unmet"] = (
        df_new.groupby(["Store","Dept"])["unmet_demand"]
        .shift(1)
        .fillna(0)
    )

    df_new["allocated_inventory"] = (
        df_new["allocated_inventory"] +
        feedback_strength * df_new["prev_unmet"]
    )

    return df_new