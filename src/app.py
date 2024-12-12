from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from utils import total_km, total_calories, total_workouts
from graphs import workouts_per_month

df = pd.read_csv("../data/raw/training_data.csv")

app = Dash(__name__)

app.layout = html.Div([
    html.Script(src='assets/script.js'),
    html.Div(
        id="section1",
        children=[
            html.Div(id='stats-div', children=[
                html.Div([
                    html.Img(src='/assets/media/running.png'),
                    html.H3("Total Distance (km):"),
                    html.Div(className='display-total', id='total-km', children=f"{total_km(df)} km")
                ], className='card'),
                html.Div([
                    html.Img(src='/assets/media/flame.png'),
                    html.H3("Total Calories Burned:"),
                    html.Div(className='display-total', id='total-calories', children=f"{total_calories(df)} kcal")
                ], className='card'),
                html.Div([
                    html.Img(src='/assets/media/calendar.png'),
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
                id='trend-line-graph-container',
                children=[
                    dcc.Graph(figure=workouts_per_month(df))
                ]
            )
        ]
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)