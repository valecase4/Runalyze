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

def workout_distribution_by_distance(df):
    from utils import count_workouts_by_distance_category

    workouts_per_category = count_workouts_by_distance_category(df)

    fig = px.bar(
        x=workouts_per_category.values(),
        y=[f"{category}    " for category in workouts_per_category.keys()], # Add some right spaces to distance yticks and bars
        orientation='h',
        title="Workout Distribution",
        color=workouts_per_category.values(),
        color_continuous_scale=["#6BAEDF", "#4C8FD2", "#3E6AA6", "#2E4A75", "#202A44"],
    )

    annotations = []

    for i, (category, value) in enumerate(workouts_per_category.items()):
        annotations.append(dict(
            x=value/2,
            y=f"{category}    ",
            text=str(value),
            font=dict(size=16,color='white'),
            showarrow=False
        ))

    fig.update_traces(
        hovertemplate="<b>Distance Category</b> %{y}<br>"
                      "<b>Workouts Completed:</b> %{x}<br>",
        marker=dict(line=dict(width=0))
    )

    fig.update_layout(
        xaxis_title="Number of Workouts",
        yaxis_title="Distance categories",
        title=dict(font=dict(size=20, color="white"), x=0.5),  # Centered title
        xaxis=dict(
            title=dict(font=dict(size=14, color="white")),
            tickfont=dict(size=18, color="white"),
            gridcolor="rgba(50, 50, 50, 0.6)",  # Subtle gridlines
        ),
        yaxis=dict(
            title=dict(font=dict(size=14, color="white")),
            tickfont=dict(size=18, color="white"),
            gridcolor="rgba(50, 50, 50, 0.6)",
            # padding=10
        ),
        plot_bgcolor="rgba(0, 0, 0, 0)",  # Transparent plot background
        paper_bgcolor="rgba(20, 20, 30, 1)",  # Dark blue-ish background,
        annotations=annotations,
        coloraxis_colorbar=dict(
            title="Workouts",
            titlefont=dict(size=16, color='white'),
            tickfont=dict(size=12, color='white'),
            tickcolor="white"
        ),
        hoverlabel=dict(
            font_size=16,
            font_color="white",
            bordercolor="rgba(100,100,255,0.8)",
        )
    )

    return fig

def average_pace_workouts(df):
    from utils import convert_pace_to_seconds, seconds_to_minutes

    new_df = convert_pace_to_seconds(df)
    workout_ids = new_df["Workout ID"]
    average_paces = new_df["Average Pace (sec/km)"]

    fig = px.line(
        x=workout_ids,
        y=average_paces,
        markers=True,
    )

    tickvals = [i for i in range(180,420,30)]
    ticktext = [seconds_to_minutes(i) for i in tickvals]

    fig.update_layout(
        yaxis=dict(
            tickvals = tickvals,
            ticktext = ticktext
        )
    )

    fig.add_shape(
        type='line',
        x0=min(workout_ids),
        x1=max(workout_ids),
        y0=240,
        y1=240,
        line=dict(color="green", width=2)
    )

    fig.add_annotation(
        x=workout_ids[len(workout_ids) // 2],
        y=235,
        text="Target: 04:00 min/km",
        showarrow=False,
        font=dict(color="green", size=14),
        align="center",
    )

    return fig