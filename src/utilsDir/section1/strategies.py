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
        last_year = df['Date'].dt.year.max()
        return df[df['Date'].dt.year == last_year]
    
class LastMonthStrategy(BaseStrategy):
    """Strategy for calculating totals for the last month."""
    def filter_data(self, df):
        last_date = df['Date'].max()
        return df[(df['Date'].dt.year == last_date.year) & (df['Date'].dt.month == last_date.month)]