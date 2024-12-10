from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from dash_extensions import EventListener

df = pd.read_csv("data/raw/training_data.csv")

def calculate_totals():
    total_km = df['Distance (km)'].sum()
    total_calories = df['Calories (kcal)'].sum()
    total_workouts = df.shape[0]
    return round(total_km, 2), round(total_calories, 2), total_workouts

app = Dash()

app.layout = html.Div(

    children=[
        # html.Script(src="assets/script.js"), 
        html.H1("Workout Data Overview"),

        html.Div(
            id="content", 
            children=[
                html.H3('Total Distance (km): '),
                html.Div(id='total-km',children=calculate_totals()[0]),

                html.H3('Total Calories Burned:'),
                html.Div(id='total-calories', children=calculate_totals()[1]),

                html.H3("Total Workouts Performed: "),
                html.Div(id='total-workouts', children=calculate_totals()[2]),
            ],
        ),
        html.Button('Update Data', id='update-button', n_clicks=0),
        html.H1("Section 2: ", id='section-2'),
    ],
)

app.layout.children.append(
    EventListener(
        id='listener', 
        events=[{'event': 'click', 'element': 'button'}], 
        callback='console.log("Ciao")',
    )
)

if __name__ == '__main__':
    app.run_server(debug=True)