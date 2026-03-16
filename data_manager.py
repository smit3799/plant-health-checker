import pandas as pd
import os


#A class to manage loading and retrieving plant health data.
class PlantDataManager:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.data = None

    def load_dataset(self):
        # Reads the CSV file using Pandas and stores it in self.data.
        # Returns true if successful, false if the file is not found.
        try:
            # Using pandas to read the file (Advanced Module Requirement)
            self.data = pd.read_csv(self.csv_path)
            print("Success: Dataset loaded!")
            return True
        except FileNotFoundError:
            print(f"Error: The file at {self.csv_path} was not found.")
            return False

    # Returns the entire dataframe.
    def get_all_data(self):
        return self.data
