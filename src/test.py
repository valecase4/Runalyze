import pandas as pd
from utils import get_monthly_workouts

df = pd.read_csv("../data/raw/training_data.csv")

temp_range = get_monthly_workouts(df)

print(temp_range)
