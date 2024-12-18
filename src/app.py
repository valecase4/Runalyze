import dash
from dash import Dash, html, dcc, callback, Output, Input, State
import plotly.express as px
import pandas as pd
from utils import *
from utilsDir.section1.main import SectionOne
from utilsDir.section1.strategies import FullDatasetStrategy, LastYearStrategy, LastMonthStrategy
from graphs import *
from dash.dash_table import DataTable

df = pd.read_csv("../data/raw/training_data.csv")

section_one = SectionOne(df, FullDatasetStrategy())

app = Dash(__name__)

app.layout = html.Div([
    html.Div(
        id="section1",
        children=[
            html.H1("Data Overview", id='section-1__title', className='section-title'),
            dcc.Dropdown(
                    options=[
                        {'label': 'General', 'value': 'general'},
                        {'label': 'Last Year', 'value': 'last_year'},
                        {'label': 'Last Month', 'value': 'last_month'},
                    ],
                    id='section-1__dropdown',
                    value='general',
                    className="overview-dropdown"
                ),
            html.Div(
                id='section-1__stats', 
                children=[
                    html.Div(
                        children=[
                            html.Img(src='/assets/media/running_colored.png', className="card__icon"),
                            html.H3("Total Distance (km):", className="card__title"),
                            html.Div(className='card__value', id='total-km', children=f"{section_one.get_total_km()} km")
                        ], 
                        className='stats-card'
                        ),
                        html.Div(
                            children=[
                                html.Img(src='/assets/media/flame_colored.png', className="card__icon"),
                                html.H3("Total Calories Burned:", className="card__title"),
                                html.Div(className='card__value', id='total-calories', children=f"{section_one.get_total_calories()} kcal")
                            ], 
                            className='stats-card'),
                        html.Div([
                            html.Img(src='/assets/media/calendar_colored.png', className="card__icon"),
                            html.H3("Workouts Performed:", className="card__title"),
                            html.Div(className='card__value', id='total-workouts', children=section_one.get_total_workouts())
                        ], 
                        className='stats-card hoverable',
                        id='card-total-workouts'
                        )
            ]),
            html.Button(
                id='section-1__add-new-workout',
                children=[
                    "Add New"
                ],
                title='Add New Workout'
            )
        ]
    ),
    html.Div(
        id="section-1__overlay",
        className="overlay hidden",
        children=[
            html.Div(
                id='section-1__data-container',
                children=[
                    html.Button(
                        "General",
                        id="filter-data__general-btn",
                        className='filter-btn'
                    ),
                    html.Button(
                        "Last Year",
                        id="filter-data__last-year-btn",
                        className='filter-btn'
                    ),
                    html.Button(
                        "Last Month",
                        id="filter-data__last-month-btn",
                        className='filter-btn'
                    ),
                    DataTable(
                        id="workout-dataset-table",
                        columns=[{"name": i, "id": i} for i in df[['Workout ID', 'Date', 'Distance (km)', 'Calories (kcal)', 'Average Pace (min/km)']].columns],
                        data=df.to_dict('records'),
                        style_header={
                            'backgroundColor': '#1f2c34',
                            'color': 'white',
                            'fontWeight': 'bold',
                            'padding': '10px',
                        },
                        style_cell={
                            'backgroundColor': '#2c2f33',
                            'color': 'white',
                            'textAlign': 'center',
                            'padding': '10px'
                        }
                    )
                ]
            ),
            html.Div(
                id='section-1__add-new-container',
                children=[
                    html.H3("Test: Add New Workout")
                ]
            ),
            html.Button(
                children="x",
                id="section-1__close-overlay-btn"
            )
        ]
    ),
    html.Div(
        id='section2',
        children=[
            html.Div(
                id='container-section-2',
                children=[
                    html.Div(
                        id='longest-workout-container',
                        children=[
                            html.Img(src='/assets/media/trend.png', style={"cursor": "pointer"}),
                            html.Div(
                                children=[
                                    html.P("Longest Workout", 
                                           style={"fontWeight": "bold", "color":"white", "fontSize": "20px", "cursor": "pointer"}
                                           ),
                                    html.P(f"{get_longest_workout(df)}", 
                                           style={"fontWeight": "500", "color": "white", "cursor": "pointer"}
                                           )
                                ]
                            )
                        ]
                    ),
                    html.Div(
                        id='section-2-title',
                        children=[
                            html.H3("Workout Distribution By Distance")
                        ]
                    ),
                    html.Div(
                        id='section-2-graph',
                        children=[
                            html.Div(
                                className="graph",
                                children=[
                                    dcc.Graph(figure=workout_distribution_by_distance(df))
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    ),
    html.Div(
        id='section3',
        children=[
            html.Div(
                id='container-section-3',
                children=[
                    html.Div(
                        id='set-goal-container',
                        children=[
                            html.Img(src='/assets/media/goal.png', style={"cursor": "pointer"}),
                            html.Div(
                                children=[
                                    html.P("Your Goal", 
                                           style={"fontWeight": "bold", "color":"white", "fontSize": "20px", "cursor": "pointer"}
                                           ),
                                    html.P("5 km - 20:00", 
                                           style={"fontWeight": "500", "color": "white", "cursor": "pointer"}
                                           )
                                ]
                            )
                        ]
                    ),
                    html.Div(
                        id='section-3-title',
                        children=[
                            html.H3("Average Pace (min/km) per Workout")
                        ]
                    ),
                    html.Div(
                        id='section-3-graph',
                        children=[
                            html.Div(
                                className="graph",
                                children=[
                                    dcc.Graph(figure=average_pace_workouts(df))
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    ),
    # html.Div(
    #     id="section4",
    #     children=[
    #     dcc.Dropdown(
    #         id="workout-selector",
    #         options=[{"label": f"Workout {row['Workout ID']} - {row['Date']}",
    #                  "value": row["Workout ID"]} for _, row in df.iterrows()],
    #         placeholder="Select a workout"
    #     ),
    #     html.Div(id='workout-details', style={"margin-top": "200px"})
    # ])
    html.Div(
        id="section4",
        children=[
            html.Div(
                id="container-section-4",
                children=[
                    html.Div(
                        id="sub-container-section-4",
                        children=[
                            html.Img(src='/assets/media/details.png', style={"cursor": "pointer"}),
                            html.Div(
                                children=[
                                    html.P("Select A Workout", 
                                           style={"fontWeight": "bold", "color":"white", "fontSize": "20px", "cursor": "pointer"}
                                           ),
                                    html.P("Workout Details", 
                                           style={"fontWeight": "500", "color": "white", "cursor": "pointer"}
                                           )
                                ]
                            )
                        ]
                    ),
                    html.Div(
                        id="main",
                        children=[
                            html.Div(
                            id='left-sideBar',
                            children=[
                                dcc.Dropdown(
                                    id="workout-selector",
                                    # options=[{"label": f"ID {row['Workout ID']} - {row['Date'].strftime("%y/%m/%d")}",
                                    #         "value": row["Workout ID"]} for _, row in df.iterrows()],
                                    placeholder="Select a workout"
                                )
                            ]
                            ),
                            html.Div(
                                id='workout-details',
                                children=[
                                    html.Div(
                                        id='main-stats-div',
                                        children=[
                                            html.H3("Main Stats"),
                                            html.Div(
                                                children=[
                                                    html.Div(
                                                        className="row-details",
                                                        children=[
                                                            html.Div(
                                                                className="details-card",
                                                                id="selected-workout-id"
                                                            ),
                                                            html.Div(
                                                                className="details-card",
                                                                id='selected-workout-date'
                                                            ),
                                                            html.Div(
                                                                className="details-card",
                                                                id='selected-workout-distance'
                                                            ),
                                                            html.Div(
                                                                className="details-card",
                                                                id='selected-workout-duration'
                                                            )
                                                        ]
                                                    ),
                                                    html.Div(
                                                        className='row-details',
                                                        children=[
                                                            html.Div(
                                                                className="details-card",
                                                                id="selected-workout-calories"
                                                            ),
                                                            html.Div(
                                                                className="details-card",
                                                                id="selected-workout-averagepace"
                                                            ),
                                                            html.Div(
                                                                className="details-card",
                                                                id="selected-workout-averagespeed"
                                                            ),
                                                            html.Div(
                                                                className="details-card",
                                                                id="selected-workout-maxspeed"
                                                            )
                                                        ]
                                                    )
                                                ]
                                            )
                                        ]
                                    ),
                                    html.Div(
                                        id="other-stats-div",
                                        children=[
                                            html.H3("Other Stats"),
                                            html.Div(
                                                children=[
                                                    html.Div(
                                                        className="row-details",
                                                        children=[
                                                            html.Div(
                                                                className="details-card",
                                                                id='selected-workout-elevationgain'
                                                            ),
                                                            html.Div(
                                                                className="details-card",
                                                                id="selected-workout-elevationloss"
                                                            ),
                                                            html.Div(
                                                                className="details-card",
                                                                id="selected-workout-startime"
                                                            )
                                                        ]
                                                    ),
                                                ]
                                            )
                                        ]
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )
    # html.Div(
    #     id='section3',
    #     children=[
    #         grid
    #     ]
    # )
])

@app.callback(
        [Output(component_id='section-1__add-new-container', component_property='className', allow_duplicate=True),
         Output(component_id='section-1__data-container', component_property='className', allow_duplicate=True),
         Output(component_id='section-1__overlay', component_property='className', allow_duplicate=True)],
        Input(component_id='section-1__add-new-workout', component_property='n_clicks'),
        prevent_initial_call=True
)
def open_new_workout_form(n_clicks):
    if n_clicks and n_clicks > 0:
        return ["", "hidden", "overlay"]
    return ["hidden", "hidden", "hidden"]

@app.callback(
    Output('workout-dataset-table', 'data'),
    [Input('filter-data__general-btn', 'n_clicks'),
     Input('filter-data__last-year-btn', 'n_clicks'),
     Input('filter-data__last-month-btn', 'n_clicks')]
)
def update_tables(general_clicks, last_year_clicks, last_month_clicks):
    ctx = dash.callback_context

    if not ctx.triggered:
        return df.to_dict('records')

    button_id = ctx.triggered[0]['prop_id'].split(".")[0]

    if button_id == 'filter-data__last-year-btn':
        return df[pd.to_datetime(df['Date']).dt.year == 2024].to_dict('records')
    
    elif button_id == 'filter-data__last-month-btn':
        return df[(pd.to_datetime(df['Date']).dt.month == 12) & (pd.to_datetime(df['Date']).dt.year == 2024)].to_dict('records')
    
    return df.to_dict('records')


@app.callback(
    Output(component_id='section-1__overlay', component_property="className", allow_duplicate=True),
    Input(component_id="section-1__close-overlay-btn", component_property="n_clicks"),
    prevent_initial_call=True
)
def close_overlay(n_clicks):
    if n_clicks and n_clicks > 0:
        return "overlay hidden"
    return "overlay"

@app.callback(
    [Output(component_id='section-1__add-new-container', component_property='className', allow_duplicate=True),
     Output(component_id='section-1__data-container', component_property='className', allow_duplicate=True),
     Output(component_id='section-1__overlay', component_property='className', allow_duplicate=True)],
    Input(component_id='card-total-workouts', component_property='n_clicks'),
    State(component_id='section-1__overlay', component_property='className'),
    prevent_initial_call=True
)
def toggle_overlay(n_clicks, current_style):
    if n_clicks and n_clicks > 0:
        return ["hidden", "", "overlay"]
    return ["hidden", "hidden", "hidden"]

# @app.callback(
#     Output(component_id='section-1__overlay', component_property="className", allow_duplicate=True),
#     Input(component_id='section-1__overlay', component_property='n_clicks'),
#     prevent_initial_call=True
# )
# def close_overlay(n_clicks):
#     if n_clicks and n_clicks > 0:
#         return "overlay hidden"
#     return "overlay"

@app.callback(
    [Output('total-km', component_property='children'),
    Output('total-calories', component_property='children'),
    Output('total-workouts', component_property='children'),
    Output('section-1__title', component_property='children')
    ],
    [Input('section-1__dropdown', component_property='value')]
)
def update_overview(value):
    strategy_map = {
        "full": FullDatasetStrategy(),
        "last_year": LastYearStrategy(),
        "last_month": LastMonthStrategy(),
    }

    selected_strategy = strategy_map.get(value, FullDatasetStrategy())
    section_one = SectionOne(df, selected_strategy)

    total_km = section_one.get_total_km()
    total_calories = section_one.get_total_calories()
    total_workouts = section_one.get_total_workouts()

    output_title = ""

    if value == "general":
        output_title = "Overview"
    elif value == "last_year":
        output_title = f"Overview: {section_one.get_last_year()}"
    else:
        output_title = f"Overview: {section_one.get_last_month()} {section_one.get_last_year()}"

    # print(value, selected_strategy)

    return [
        f"{total_km}",
        f"{total_calories}",
        f"{total_workouts}",
        f"{output_title}"
    ]

# @app.callback(
#     [
#         Output(component_id='selected-workout-id', component_property="children"),
#         Output(component_id='selected-workout-date', component_property='children'),
#         Output(component_id='selected-workout-distance', component_property="children"),
#         Output(component_id='selected-workout-duration', component_property="children"),
#         Output(component_id='selected-workout-calories', component_property="children"),
#         Output(component_id='selected-workout-averagepace', component_property='children'),
#         Output(component_id='selected-workout-averagespeed', component_property="children"),
#         Output(component_id='selected-workout-maxspeed', component_property="children"),
#         Output(component_id='selected-workout-elevationgain', component_property="children"),
#         Output(component_id='selected-workout-elevationloss', component_property="children"),
#         Output(component_id="selected-workout-startime", component_property="children")
#     ],
#     [Input(component_id="workout-selector", component_property="value")]
# )
# def update_workout_details(selected_id):
#     # if selected_id is None:
#     #     return "Please select a workout to see details."
    
#     # workout = df[df["Workout ID"] == selected_id].iloc[0]
#     print(workout["Elevation Gain (m)"])
#     print(type(workout["Elevation Gain (m)"]))

#     return [
#         html.Div(
#             children=[
#                 html.H5("Workout ID"),
#                 html.P(f"{workout["Workout ID"]}")
#             ]
#         ),
#         html.Div(
#             children=[
#                 html.H5("Date"),
#                 html.P(f"{workout["Date"].strftime("%y-%m-%d")}")
#             ]
#         ),
#         html.Div(
#             children=[
#                 html.H5("Distance"),
#                 html.P(f"{workout["Distance (km)"]} km")
#             ]
#         ),
#         html.Div(
#             children=[
#                 html.H5("Duration"),
#                 html.P(f"{workout["Duration (min)"]}")
#             ]
#         ),
#         html.Div(
#             children=[
#                 html.H5("Calories"),
#                 html.P(f"{workout["Calories (kcal)"]}kcal")
#             ]
#         ),
#         html.Div(
#             children=[
#                 html.H5("Average Pace"),
#                 html.P(f"{workout["Average Pace (min/km)"]}min/km")
#             ]
#         ),
#         html.Div(
#             children=[
#                 html.H5("Average Speed"),
#                 html.P(f"{workout["Average Speed (km/h)"]}km/h")
#             ]
#         ),
#         html.Div(
#             children=[
#                 html.H5("Max Speed"),
#                 html.P(f"{workout["Max Speed (km/h)"]}km/h")
#             ]
#         ),
#         html.Div(
#             children=[
#                 html.H5("Elevation Gain"),
#                 html.Img(src='/assets/media/elevation-gain.png'),
#                 html.P(f"{workout["Elevation Gain (m)"]}m" if f"{workout["Elevation Gain (m)"]}" != "nan" else "-")
#             ]
#         ),
#         html.Div(
#             children=[
#                 html.H5("Elevation Loss"),
#                 html.Img(src='/assets/media/elevation-loss.png'),
#                 html.P(f"{workout["Elevation Loss (m)"]}m" if f"{workout["Elevation Loss (m)"]}" != "nan" else "-")
#             ]
#         ),
#         html.Div(
#             children=[
#                 html.H5("Start Time"),
#                 html.Img(src='/assets/media/watch.png'),
#                 html.P(f"{workout["Start Time"]}")
#             ]
#         )
#     ]

    # return html.Div(
    #     className="workout-details-row",
    #     children=[
    #         html.Div(
    #             className="workout-details-card",
    #             children=[
    #                 html.Img(src="/assets/media/temperature.png"),
    #                 html.P("Temperature (C)"),
    #                 html.P(f"{workout["Temperature (C)"]}")
    #             ]
    #         ),
    #         html.Div(
    #             className="workout-details-card",
    #             children=[
    #                 html.Img(src="/assets/media/wind.png"),
    #                 html.P("Wind Speed (km/h)"),
    #                 html.P(f"{workout["Wind Speed (km/h)"]}")
    #             ]
    #         ),
    #         html.Div(
    #             className="workout-details-card",
    #             children=[
    #                 html.Img(src="/assets/media/humidity.png"),
    #                 html.P("Humidity (%)"),
    #                 html.P(f"{workout["Humidity (%)"]}")
    #             ]
    #         )
    #     ]
    # )
    # return html.Div([
    #     html.H3(f"Workout Details (ID: {workout['Workout ID']})"),
    #     html.P(f"Date: {workout['Date']}"),
    #     html.P(f"Distance: {workout['Distance (km)']} km"),
    #     html.P(f"Duration: {workout['Duration (min)']} min"),
    #     html.P(f"Calories Burned: {workout['Calories (kcal)']} kcal"),
    # ])

if __name__ == '__main__':
    app.run_server(debug=True)