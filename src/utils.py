import pandas as pd

def total_km(df):
    return round(df['Distance (km)'].sum(), 2)

def total_calories(df):
    return df['Calories (kcal)'].sum()

def total_workouts(df):
    return df.shape[0]

def get_workouts_per_year(df):
    df['Date'] = pd.to_datetime(df['Date'])
    workouts_per_year = df.groupby(df['Date'].dt.year).size()
    return workouts_per_year