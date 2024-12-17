from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from utils import *
from utilsDir.section1.main import SectionOne
from graphs import *
import dash_ag_grid as dag

df = pd.read_csv("../data/raw/training_data.csv")

section_one = SectionOne(df)

app = Dash(__name__)

# Try Dataframe

dataFrame = pd.DataFrame({
    "Workout ID": [1, 2, 3],
    "Date": ["2024-12-01", "2024-12-02", "2024-12-03"],
    "Distance (km)": [5.0, 7.2, 10.0],
    "Duration (min)": [25, 35, 50],
    "Calories (kcal)": [300, 400, 600],
})

######### TRYINH DASH-AS-GRID COMPONENT LIBRARY

grid = dag.AgGrid(
    id='get-started',
    rowData=df.to_dict("records"),
    columnDefs=[
        {"field": "Date", "sortable": True, "filter": True},
        {"field": "Average Pace (min/km)", "sortable": True, "filter": True},
        {"field": "Distance (km)", "sortable": True, "filter": True}
    ],
    className="ag-theme-alpine-dark"
)

app.layout = html.Div([
    html.Script(src='assets/script.js'),
    html.Div(
        id="section1",
        children=[
            html.H1("Data Overview", id='title-section-1'),
            dcc.Dropdown([
                'General', 
                f'Last Month: {get_last_month(df)}',
                f'Last Year: {get_last_year(df)}'
                ], 
                id='select-overview',
                value='General'
                ),
            html.Div(id='stats-div', children=[
                html.Div([
                    html.Img(src='/assets/media/running_colored.png'),
                    html.H3("Total Distance (km):"),
                    html.Div(className='display-total', id='total-km', children=f"{section_one.get_total_km()} km")
                ], className='card'),
                html.Div([
                    html.Img(src='/assets/media/flame_colored.png'),
                    html.H3("Total Calories Burned:"),
                    html.Div(className='display-total', id='total-calories', children=f"{section_one.get_total_calories()} kcal")
                ], className='card'),
                html.Div([
                    html.Img(src='/assets/media/calendar_colored.png'),
                    html.H3("Workouts Performed:"),
                    html.Div(className='display-total', id='total-workouts', children=section_one.get_total_workouts())
                ], className='card')
            ])
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
                                    options=[{"label": f"ID {row['Workout ID']} - {row['Date'].strftime("%y/%m/%d")}",
                                            "value": row["Workout ID"]} for _, row in df.iterrows()],
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

# Manage dropdown menu behavior

@app.callback(
    Output('total-km', component_property='children'),
    Output('total-calories', component_property='children'),
    Output('total-workouts', component_property='children'),
    Output('title-section-1', component_property='children'),
    Input('select-overview', component_property='value')
)
def update_overview(value):
    if value != 'General':
        my_value = value.split(":")[1].strip()
        
        if len(my_value.split(" ")) == 2:
            last_month, last_year = get_month_index_by_name(my_value.split(" ")[0]), int(my_value.split(" ")[1])
            return [
                f"{total_km_last_month(df, last_month, last_year)}",
                f"{total_calories_last_month(df, last_month, last_year)}",
                f"{total_workouts_last_month(df, last_month, last_year)}",
                f"Overview of Your Last Month: {last_month, last_year}"
            ]
        else:
            last_year = int(my_value)
            return [
                f"{total_km_last_year(df, last_year)}", 
                f"{total_calories_last_year(df, last_year)}",
                f"{total_workouts_last_year(df, last_year)}",
                f"Overview of Your Last Year: {last_year}"
            ]
        
        # if len(value.split(" ")) == 2: # last month (e.g. Dec 2024)
        #     print(value)
        # else:
        #     last_year = int(str(value.split(":")[-1]).strip())
        #     print(last_year)
        #     return [
        #         f"{total_km_last_year(df, last_year)}", 
        #         f"{total_calories_last_year(df, last_year)}",
        #         f"{total_workouts_last_year(df, last_year)}",
        #         f"Overview of Your Last Year: {last_year}"
        #     ]
    else:
        return [
            section_one.get_total_km(), 
            section_one.get_total_calories(),
            section_one.get_total_workouts(),
            "Overview"
        ]

@app.callback(
    [
        Output(component_id='selected-workout-id', component_property="children"),
        Output(component_id='selected-workout-date', component_property='children'),
        Output(component_id='selected-workout-distance', component_property="children"),
        Output(component_id='selected-workout-duration', component_property="children"),
        Output(component_id='selected-workout-calories', component_property="children"),
        Output(component_id='selected-workout-averagepace', component_property='children'),
        Output(component_id='selected-workout-averagespeed', component_property="children"),
        Output(component_id='selected-workout-maxspeed', component_property="children"),
        Output(component_id='selected-workout-elevationgain', component_property="children"),
        Output(component_id='selected-workout-elevationloss', component_property="children"),
        Output(component_id="selected-workout-startime", component_property="children")
    ],
    [Input(component_id="workout-selector", component_property="value")]
)
def update_workout_details(selected_id):
    # if selected_id is None:
    #     return "Please select a workout to see details."
    
    workout = df[df["Workout ID"] == selected_id].iloc[0]
    print(workout["Elevation Gain (m)"])
    print(type(workout["Elevation Gain (m)"]))

    return [
        html.Div(
            children=[
                html.H5("Workout ID"),
                html.P(f"{workout["Workout ID"]}")
            ]
        ),
        html.Div(
            children=[
                html.H5("Date"),
                html.P(f"{workout["Date"].strftime("%y-%m-%d")}")
            ]
        ),
        html.Div(
            children=[
                html.H5("Distance"),
                html.P(f"{workout["Distance (km)"]} km")
            ]
        ),
        html.Div(
            children=[
                html.H5("Duration"),
                html.P(f"{workout["Duration (min)"]}")
            ]
        ),
        html.Div(
            children=[
                html.H5("Calories"),
                html.P(f"{workout["Calories (kcal)"]}kcal")
            ]
        ),
        html.Div(
            children=[
                html.H5("Average Pace"),
                html.P(f"{workout["Average Pace (min/km)"]}min/km")
            ]
        ),
        html.Div(
            children=[
                html.H5("Average Speed"),
                html.P(f"{workout["Average Speed (km/h)"]}km/h")
            ]
        ),
        html.Div(
            children=[
                html.H5("Max Speed"),
                html.P(f"{workout["Max Speed (km/h)"]}km/h")
            ]
        ),
        html.Div(
            children=[
                html.H5("Elevation Gain"),
                html.Img(src='/assets/media/elevation-gain.png'),
                html.P(f"{workout["Elevation Gain (m)"]}m" if f"{workout["Elevation Gain (m)"]}" != "nan" else "-")
            ]
        ),
        html.Div(
            children=[
                html.H5("Elevation Loss"),
                html.Img(src='/assets/media/elevation-loss.png'),
                html.P(f"{workout["Elevation Loss (m)"]}m" if f"{workout["Elevation Loss (m)"]}" != "nan" else "-")
            ]
        ),
        html.Div(
            children=[
                html.H5("Start Time"),
                html.Img(src='/assets/media/watch.png'),
                html.P(f"{workout["Start Time"]}")
            ]
        )
    ]

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