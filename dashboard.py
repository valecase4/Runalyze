from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from dash_extensions import EventListener
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import DashProxy, State

df = pd.read_csv("data/raw/training_data.csv")

app = Dash()

if __name__ == '__main__':
    app.run_server(debug=True)