def get_store_selection(st, df):
    all_stores = sorted(df["Store"].unique())

    select_all_stores = st.sidebar.checkbox("Select All Stores", value=True)

    if select_all_stores:
        selected_stores = all_stores
    else:
        selected_stores = st.sidebar.multiselect(
            "Select Store(s)",
            options=all_stores,
            default=[all_stores[0]]
        )

    if not selected_stores:
        st.warning("Please select at least one store.")
        st.stop()

    return selected_stores


def get_department_selection(st, df, selected_stores, view_mode):

    available_depts = sorted(
        df[df["Store"].isin(selected_stores)]["Dept"].unique()
    )

    if view_mode == "Entire Store View":
        selected_depts = available_depts
        st.sidebar.info("All departments for selected store(s) included.")
    else:
        select_all_depts = st.sidebar.checkbox("Select All Departments", value=True)

        if select_all_depts:
            selected_depts = available_depts
        else:
            selected_depts = st.sidebar.multiselect(
                "Select Department(s)",
                options=available_depts,
                default=[available_depts[0]] if available_depts else []
            )

    if not selected_depts:
        st.warning("No departments available for selection.")
        st.stop()

    return selected_depts, available_depts
