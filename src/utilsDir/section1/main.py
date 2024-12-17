class SectionOne:
    def __init__(self, df):
        self.df = df

    def get_total_km(self):
        return round(self.df['Distance (km)'].sum(), 2)
        
    def get_total_calories(self):
        calories = self.df['Calories (kcal)'].sum()
        formatted_calories = f"{calories:,}".replace(",", ".")
        return formatted_calories
    
    def get_total_workouts(self):
        return self.df.drop_duplicates(subset='Date', keep='first').shape[0]