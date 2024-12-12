from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from utils import total_km, total_calories, total_workouts

df = pd.read_csv("../data/raw/training_data.csv")

app = Dash(__name__)

app.layout = html.Div([
    html.Script(src='assets/script.js'),
    html.Div(
        id="section1",
        children=[
            html.H1("Workout Data Analysis"),
            html.Div(id='stats-div', children=[
                html.Div([
                    html.H3("Total Distance (km):"),
                    html.Div(className='display-total', id='total-km', children=total_km(df))
                ], className='card'),
                html.Div([
                    html.H3("Total Calories Burned:"),
                    html.Div(className='display-total', children=total_calories(df))
                ], className='card'),
                html.Div([
                    html.H3("Workouts Performed:"),
                    html.Div(className='display-total', children=total_workouts(df))
                ], className='card')
            ])
        ]
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)