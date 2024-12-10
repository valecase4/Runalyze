from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

df = pd.read_csv("data/raw/training_data.csv")

def calculate_totals():
    total_km = df['Distance (km)'].sum()
    total_calories = df['Calories (kcal)'].sum()
    return round(total_km, 2), round(total_calories, 2)

app = Dash()

app.layout = html.Div(
    children=[
        html.H1("Workout Data Overview"),

        html.Div(
            id="content", 
            children=[
                html.H3('Total Distance (km): ', style={'color': 'white'}),
                html.Div(id='total-km',children=calculate_totals()[0]),

                html.H3('Total Calories Burned:', style={'color': 'white'}),
                html.Div(id='total-calories', children=calculate_totals()[1]),
            ],
        ),
        html.Button('Update Data', id='update-button', n_clicks=0)
    ],
)

if __name__ == '__main__':
    app.run_server(debug=True)