def total_km(df):
    return round(df['Distance (km)'].sum(), 2)

def total_calories(df):
    return df['Calories (kcal)'].sum()

def total_workouts(df):
    return df.shape[0]