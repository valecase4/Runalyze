import pandas as pd

# def total_km(df):
#     return round(df['Distance (km)'].sum(), 2)

# def total_calories(df):
#     calories = df['Calories (kcal)'].sum()
#     formatted_value = f"{calories:,}".replace(",", ".")
#     return formatted_value

# def total_workouts(df):
#     return df.drop_duplicates(subset='Date', keep='first').shape[0]

def get_month_index_by_name(month_name):
    month_values = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12 
    }

    return month_values[month_name]

def total_km_last_month(df, last_month, last_year):
    """
    Calculate the sum of kilometers for the workouts performed 
    during the last month
    """
    filtered = df[(df['Date'].dt.month == last_month) & (df['Date'].dt.year == last_year)]
    return round(filtered['Distance (km)'].sum(), 2)

def total_calories_last_month(df, last_month, last_year):
    """
    Calculate the sum of calories burned for the workouts performed 
    during the last month
    """
    filtered = df[(df['Date'].dt.month == last_month) & (df['Date'].dt.year == last_year)]
    return filtered['Calories (kcal)'].sum()

def total_workouts_last_month(df, last_month, last_year):
    """
    Calculate the number of workouts performed
    during the last month
    """
    filtered = df[(df['Date'].dt.month == last_month) & (df['Date'].dt.year == last_year)].drop_duplicates(subset='Date', keep='first')
    return filtered.shape[0]

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
    filtered = df[df['Date'].dt.year == last_year].drop_duplicates(subset='Date', keep='first')
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
    return last_date.strftime('%b %Y')

def get_longest_workout(df):
    """
    Return distance and duration of the longest workout in the dataset
    """
    best_row= df.sort_values("Distance (km)", ascending=False).iloc[0]
    return f"{best_row['Distance (km)']} km - {best_row['Duration (min)']}"

def get_distance_category(distance):
    """
    Assign a distance category based on the input distance.

    Categories:
    - 0-2 km
    - 2-4 km
    - 4-6 km
    - 6-8 km
    - 8-10 km

    Parameters:
        distance (float): The distance value in kilometers.

    Returns:
        str: The category label (e.g., '0-2 km') or 'Unknown' if out of range.
    """
    distance = int(distance)
    if 0 <= distance < 2:
        return '0-2 km'
    elif 2 <= distance < 4:
        return '2-4 km'
    elif 4 <= distance < 6:
        return '4-6 km'
    elif 6 <= distance < 8:
        return '6-8 km'
    elif 8 <= distance <= 10:
        return '8-10 km'
    else:
        return 'Unknown'


def count_workouts_by_distance_category(df):
    """
    Calculate the distribution of workouts into distance categories.

    Categories:
    - 0-2 km
    - 2-4 km
    - 4-6 km
    - 6-8 km
    - 8-10 km

    Parameters:
        df (pd.DataFrame): The input dataframe containing a 'Distance (km)' column.

    Returns:
        dict: A dictionary where keys are category labels (e.g., '0-2 km') 
              and values are the count of workouts in each category.
    """

    df['Category'] = df['Distance (km)'].apply(get_distance_category)
    print(df.groupby("Category").size())

    category_counts = df['Category'].value_counts().sort_index()

    return dict(sorted(category_counts.to_dict().items(), key=lambda x: x[1]))

def convert_pace_to_seconds(df, pace_column: str='Average Pace (min/km)'):
    def mmss_to_seconds(pace):
        try:
            minutes, seconds = map(int, pace.split(":"))
            return minutes * 60 + seconds
        except (ValueError, AttributeError):
            return None
        
    df["Average Pace (sec/km)"] = df[pace_column].apply(mmss_to_seconds)
    df["Duration (sec)"] = df["Duration (min)"].apply(mmss_to_seconds)

    df = df[(df["Duration (sec)"] >= 1190) & (df["Duration (sec)"] <= 1210)]
    return df


def seconds_to_minutes(seconds):
    try:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{minutes:02}:{remaining_seconds:02}"
    except Exception as e:
        print(f"Error converting seconds to minutes: {e}")
        return None