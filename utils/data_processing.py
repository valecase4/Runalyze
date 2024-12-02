def duration_to_seconds(duration_str, workout_id=None):
    """
    Convert a duration string in HH:MM:SS, MM:SS, or SS format to total seconds.
    Parameters:
        duration_str (str): The duration in string format.
        workout_id (optional): ID of the workout, useful for tracking errors.
    Returns:
        int or None: The duration in seconds, or None if invalid.
    """
    try:
        elements = duration_str.split(":")
        if len(elements) == 1:  # Seconds only
            return int(elements[0])
        elif len(elements) == 2:  # MM:SS
            minutes, seconds = map(int, elements)
            return seconds + minutes * 60
        elif len(elements) == 3:  # HH:MM:SS
            hours, minutes, seconds = map(int, elements)
            return seconds + minutes * 60 + hours * 3600
        else:
            return None
    except Exception as e:
        print(f"Error converting duration '{duration_str}' for workout ID {workout_id}: {e}")
        return None

def pace_to_seconds(pace_str, workout_id=None):
    """
    Convert a pace string in MM:SS format to total seconds.
    
    Parameters:
        pace_str (str): The pace in MM:SS format (e.g., '03:45').
        workout_id (optional): ID of the workout, useful for tracking errors.
        
    Returns:
        int: The pace in seconds, or None if the format is invalid.
    """
    try:
        minutes, seconds = map(int, pace_str.split(":"))
        return minutes * 60 + seconds
    except Exception as e:
        print(f"Error converting pace '{pace_str}' for workout ID {workout_id}: {e}")
        return None

def is_valid_time_format(time_str):
    """
    Verifies if a string is in the format MM:SS, SS, or HH:MM:SS.
    
    Parameters:
        time_str (str): The string to check.
        
    Returns:
        bool: True if the format is valid, False otherwise.
    """
    if time_str.count(":") == 1:  # Possible format MM:SS
        try:
            minutes, seconds = map(int, time_str.split(":"))
            return 0 <= minutes < 60 and 0 <= seconds < 60
        except ValueError:
            return False
    elif time_str.count(":") == 2:  # Possible format HH:MM:SS
        try:
            hours, minutes, seconds = map(int, time_str.split(":"))
            return 0 <= hours < 24 and 0 <= minutes < 60 and 0 <= seconds < 60
        except ValueError:
            return False
    elif time_str.count(":") == 0:  # Possible format SS
        try:
            seconds = int(time_str)
            return 0 <= seconds < 60
        except ValueError:
            return False
    return False

def impute_missing_values(df, column_name):
    """
    Imputes missing values in a specified column based on the mean of valid values for rows with the same date.
    If no valid values are found for the same date, imputes 0.

    Parameters:
        df (pandas.DataFrame): The dataframe containing the data.
        column_name (str): The name of the column to process (e.g., 'Elevation Gain (m)', 'Temperature').
        
    Returns:
        df (pandas.DataFrame): The dataframe with missing values imputed.
    """
    missing_data = df[df[column_name].isnull()]

    for idx, row in missing_data.iterrows():
        same_date_rows = df[df['Date'] == row['Date']]

        valid_rows = same_date_rows[same_date_rows[column_name].notnull()]

        if not valid_rows.empty:
            mean_value = valid_rows[column_name].mean()
            df.at[idx, column_name] = mean_value
        else:
            df.at[idx, column_name] = 0
    
    return df