import pandas as pd

def total_km(df):
    return round(df['Distance (km)'].sum(), 2)

def total_calories(df):
    calories = df['Calories (kcal)'].sum()
    formatted_value = f"{calories:,}".replace(",", ".")
    return formatted_value

def total_workouts(df):
    return df.shape[0]

def total_km_last_year(df, last_year):
    """
    Calculate the sum of kilometers for the workouts performed 
    during the last year
    """
    filtered = df[df['Date'].dt.year == last_year]
    return round(filtered['Distance (km)'].sum(), 2)

def total_calories_last_year(df, last_year):
    """
    Calculate the sum of calories for the workouts performed 
    during the last year
    """
    filtered = df[df['Date'].dt.year == last_year]
    calories = filtered['Calories (kcal)'].sum()
    formatted_value = f"{calories:,}".replace(",", ".")
    return formatted_value

def total_workouts_last_year(df, last_year):
    """
    Calculate the number of workouts performed
    during the last year
    """
    filtered = df[df['Date'].dt.year == last_year]
    return filtered.shape[0]

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

def get_last_year(df):
    """
    Retrieve the last year available in the dataset based on the latest workout date.

    Parameters:
        df (pd.DataFrame): The input dataframe containing a 'Date' column.

    Returns:
        int: The last year available in the dataset.
    """
    df['Date'] = pd.to_datetime(df['Date'])
    return df['Date'].dt.year.max()

def get_last_month(df):
    """
    Retrieve the last month and year available in the dataset based on the latest workout date.

    Parameters:
        df (pd.DataFrame): The input dataframe containing a 'Date' column.

    Returns:
        str: The last month and year in the format 'MMM YY' (e.g., 'Dec 24').
    """
    df['Date'] = pd.to_datetime(df['Date'])
    last_date = df['Date'].max()
    return last_date.strftime('%b %y')

