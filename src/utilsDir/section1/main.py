import pandas as pd

class SectionOne:
    def __init__(self, df, strategy):
        """
        Initialize SectionOne with a dataframe and a strategy.

        Parameters:
            df (pd.DataFrame): The dataset.
            strategy (BaseStrategy): A strategy instance for filtering data.
        """
        self.df = df
        self.strategy = strategy

    def get_filtered_data(self):
        """Apply the selected strategy to filter the dataframe."""
        return self.strategy.filter_data(self.df)

    def get_total_km(self):
        """Calculate total kilometers."""
        data = self.get_filtered_data()
        return round(data["Distance (km)"].sum(), 2)
    
    def get_total_calories(self):
        """Calculate total calories burned."""
        data = self.get_filtered_data()
        calories = data['Calories (kcal)'].sum()
        return f"{calories:,}".replace(",", ".")
    
    def get_total_workouts(self):
        """Calculate total unique workouts."""
        data = self.get_filtered_data()
        return data.drop_duplicates(subset='Date', keep='first').shape[0]
    
    def get_last_year(self):
        last_year = pd.to_datetime(self.df['Date']).dt.year.max()
        return last_year
    
    def get_last_month(self):
        from ..utils import get_month_name

        last_month = pd.to_datetime(self.df["Date"]).max()
        return get_month_name(last_month.month)
    