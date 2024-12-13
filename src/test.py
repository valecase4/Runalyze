import pandas as pd
from utils import *

df = pd.read_csv("../data/raw/training_data.csv")

last_year = get_last_year(df)

print(total_calories_last_year(df, last_year))

print(count_workouts_by_distance_category(df))