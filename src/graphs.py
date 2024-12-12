import plotly.express as px

def workouts_per_month(df):
    """
    Generate a line chart showing the trend of workouts per month.

    Parameters:
        df (pd.DataFrame): The input dataframe containing workout data. Must include 'Date' column.

    Returns:
        plotly.graph_objs._figure.Figure: A Plotly figure object with the trend line.
    """
    from utils import get_monthly_workouts

    monthly_workouts = get_monthly_workouts(df)

    fig = px.line(
        x=monthly_workouts.index.to_timestamp(),
        y=monthly_workouts.values,
        labels={"x": "Month", "y": "Number of Workouts"},
        title="Monthly Workout Trend",
    )

    fig.update_traces(
        line=dict(color='cyan', width=1, dash='solid')
    )

    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Number of Workouts",
        template="plotly_dark",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        hovermode='x unified',
        margin=dict(l=40,r=20,t=60,b=40)
    )

    print("Data Type:", type(fig))
    return fig
