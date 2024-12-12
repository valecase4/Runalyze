import pandas as pd
from utils import get_monthly_workouts, total_km_last_year, get_last_year, total_calories_last_year

df = pd.read_csv("../data/raw/training_data.csv")

last_year = get_last_year(df)

print(total_calories_last_year(df, last_year))
