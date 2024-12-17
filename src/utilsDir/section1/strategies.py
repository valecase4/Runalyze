import pandas as pd

class BaseStrategy:
    """Base class for calculation strategies."""
    def filter_data(self, df):
        return df
    
class FullDatasetStrategy(BaseStrategy):
    """Strategy for calculating totals on the full dataset."""
    def filter_data(self, df):
        return df
    
class LastYearStrategy(BaseStrategy):
    """Strategy for calculating totals for the last year."""
    def filter_data(self, df):
        last_year = pd.to_datetime(df['Date']).dt.year.max()
        return df[pd.to_datetime(df['Date']).dt.year == last_year]
    
class LastMonthStrategy(BaseStrategy):
    """Strategy for calculating totals for the last month."""
    def filter_data(self, df):
        last_date = pd.to_datetime(df['Date']).max()
        df['Date'] = pd.to_datetime(df['Date'])
        return df[(df['Date'].dt.year == last_date.year) & (df['Date'].dt.month == last_date.month)]