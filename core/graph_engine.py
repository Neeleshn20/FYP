import plotly.graph_objects as go

def render_graph(st, df, show_actual, show_expected,
                 show_allocated, show_loss, show_service):

    fig = go.Figure()

    if show_actual:
        fig.add_trace(go.Scatter(
            x=df["Date"],
            y=df["Weekly_Sales"],
            name="Actual Demand",
            mode="lines"
        ))

    if show_expected:
        fig.add_trace(go.Scatter(
            x=df["Date"],
            y=df["expected_demand"],
            name="Expected Demand",
            mode="lines",
            line=dict(dash="dash")
        ))

    if show_allocated:
        fig.add_trace(go.Scatter(
            x=df["Date"],
            y=df["allocated_inventory"],
            name="Allocated Inventory",
            mode="lines"
        ))

    if show_loss:
        fig.add_trace(go.Bar(
            x=df["Date"],
            y=df["weekly_loss"],
            name="Weekly Economic Loss",
            yaxis="y2",
            opacity=0.4
        ))

    if show_service:
        fig.add_trace(go.Scatter(
            x=df["Date"],
            y=df["service_level"],
            name="Service Level",
            mode="lines",
            yaxis="y2"
        ))

    fig.update_layout(
        template="plotly_dark",
        height=600,
        yaxis=dict(title="Units"),
        yaxis2=dict(
            title="Loss / Service Level",
            overlaying="y",
            side="right"
        )
    )

    st.plotly_chart(fig, use_container_width=True)