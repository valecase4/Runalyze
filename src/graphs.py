import plotly.express as px
from utils import get_workouts_per_year

def workouts_per_year(df):
    fig = px.pie(
        data_frame=get_workouts_per_year(df), 
        title='Workouts per Year',
        values=get_workouts_per_year(df).values, 
        names=get_workouts_per_year(df).index,
        color_discrete_sequence=px.colors.sequential.RdBu_r
        )
    
    return fig