import pandas as pd

def total_km(df):
    return round(df['Distance (km)'].sum(), 2)

def total_calories(df):
    return df['Calories (kcal)'].sum()

def total_workouts(df):
    return df.shape[0]

def get_monthly_workouts(df):
    """
    Calculate the number of workouts per month, including months with no workouts.

    Parameters:
        df (pd.DataFrame): The input dataframe containing workout data. Must include a 'Date' column.

    Returns:
        pd.Series: A pandas Series with a PeriodIndex (monthly) and the number of workouts per month.
    """
    df['Date'] = pd.to_datetime(df['Date'])
    df= df.drop_duplicates(subset='Date', keep='first')

    full_range = pd.date_range(
        start=df['Date'].min().replace(day=1),
        end=df['Date'].max().replace(day=1),
        freq='MS'
    )

    full_range_index = full_range.to_period('M')

    monthly_counts = df.groupby(df['Date'].dt.to_period('M')).size()

    monthly_counts = monthly_counts.reindex(full_range_index, fill_value=0)

    return monthly_counts