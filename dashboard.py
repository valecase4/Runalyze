from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from dash_extensions import EventListener
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import DashProxy, State
import plotly.express as px

df = pd.read_csv("data/raw/training_data.csv")

app = Dash()

app.layout = html.Div([
    html.H1("Filter workouts by minimum distance"),
    html.Div(
        id='input-div',
        children=[
            dcc.Input(id='my-input', placeholder='Distance (km)', type='number', min=0, max=50),
        ]
    ),
    html.Div(id='workout-list'),
    html.Div(
        id='workouts-per-year',
        children=[
            dcc.Dropdown(options=['2023', '2024'], value='2023', id='year-input'),
            # html.Div(id='workoutsss')
            dcc.Graph(id='my-graph-output')
        ]
    ),
    html.Div(
        id='slider-div',
        children=[
            html.H1("Range Slider Section"),
            dcc.RangeSlider(
                min=df['Workout ID'].min(),
                max=df['Workout ID'].max(),
                step=1,
                marks={str(id): str(id) for id in df['Workout ID']},
                value=[df['Workout ID'].min(), df['Workout ID'].max()],
                id='input-slider'
            ),
            html.P(id='range-output')
        ]
    )
])

@callback(
    Output('range-output', 'children'),
    Input('input-slider', 'value')
)
def average_distance_per_range(range_slider_value):
    filtered_df = df[(df['Workout ID'] >= range_slider_value[0]) & (df['Workout ID'] <= range_slider_value[1])]
    average_distance = filtered_df['Distance (km)'].mean()
    return f"Average Distance for the selected Range: {round(average_distance, 2)}"

@callback(
    Output(component_id='my-graph-output', component_property='figure'),
    Input(component_id='year-input', component_property='value')
)
def wks_per_year(dropdown_value):
    # counter = 0
    # for _, row in df.iterrows():
    #     if (row['Date'].split("/")[2]) == dropdown_value:
    #         counter += 1
    # # filtered_df = df[str(df['Date']).split('/')[-1] == str(dropdown_value)]
    # # return f"In {dropdown_value} you performed {filtered_df.shape[0]}"
    # return f"In {dropdown_value} you performed {counter} workouts."

    # workouts = []

    df['Date'] = pd.to_datetime(df['Date'])
    filtered = df[df['Date'].dt.year == int(dropdown_value)]

    workouts_per_month = filtered.groupby(df['Date'].dt.month).size()
    
    # for _, row in filtered.iterrows():
    #     workouts.append(
    #         html.P(f"{row['Date']} --> {row['Distance (km)']}")
    #     )

    # return workouts

    fig = px.bar(
        workouts_per_month, 
        title=f'Number of Workouts per Month based on Year {dropdown_value}', 
    )
    fig.update_layout(transition_duration=500)

    return fig


@callback(
    Output(component_id='workout-list', component_property='children'),
    Input(component_id='my-input', component_property='value')
)
def show_filtered_workouts(input_value):
    filtered = []
    if input_value is not None:
        for _, row in df.iterrows():
            if row['Distance (km)'] >= int(input_value):
                filtered.append(
                    html.Div(
                        children=[
                            html.H4(f"Workout ID: {row['Workout ID']}"),
                            html.P(f"Date: {row['Date']}"),
                            html.P(f"Distance: {row['Distance (km)']} km"),
                            html.P(f"Calories: {row['Calories (kcal)']}"),
                        ],
                        className='workout-div'
                    )
                )
        return filtered

if __name__ == '__main__':
    app.run_server(debug=True)