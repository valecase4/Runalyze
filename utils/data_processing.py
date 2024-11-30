def duration_to_seconds(duration_str):
    """
    Convert a duration string in HH:MM:SS, MM:SS, or SS format to total seconds.
    Parameters:
        duration_str (str): The duration in string format.
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
        print(f"Error converting duration '{duration_str}': {e}")
        return None
