from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from utils import *
from graphs import *
import dash_ag_grid as dag

df = pd.read_csv("../data/raw/training_data.csv")

app = Dash(__name__)

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
                    html.Div(className='display-total', id='total-km', children=f"{total_km(df)} km")
                ], className='card'),
                html.Div([
                    html.Img(src='/assets/media/flame_colored.png'),
                    html.H3("Total Calories Burned:"),
                    html.Div(className='display-total', id='total-calories', children=f"{total_calories(df)} kcal")
                ], className='card'),
                html.Div([
                    html.Img(src='/assets/media/calendar_colored.png'),
                    html.H3("Workouts Performed:"),
                    html.Div(className='display-total', id='total-workouts', children=total_workouts(df))
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
        id="section3",
        children=[
            dcc.Graph(figure=average_pace_workouts(df), style={"width": "100%"})
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
    
@callback(
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
            total_km(df), 
            total_calories(df),
            total_workouts(df),
            "Overview"
        ]

if __name__ == '__main__':
    app.run_server(debug=True)