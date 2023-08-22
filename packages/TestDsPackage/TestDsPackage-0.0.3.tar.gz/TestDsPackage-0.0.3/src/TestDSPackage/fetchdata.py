from .exception import CustomException

import pandas as pd
import sys
import importlib.resources as resources

class FetchData:
    def __init__(self):
        self.__data_directory = "Data"  # Directory where CSV files are stored

    def load_data(self, file_name: str):
        file_name = file_name.lower() + '.csv'
        
        data_path = resources.files('TestDSPackage').joinpath(self.__data_directory, file_name)
        
        try:
            df = pd.read_csv(data_path)
            print(f"The file '{file_name}' exists in the '{self.__data_directory}' directory.")
            return df
        except FileNotFoundError as e:
            files = resources.contents('TestDSPackage.' + self.__data_directory)
            file_names = [item for item in files if item.endswith('.csv')]
            raise CustomException(f"The file '{file_name}' does not exist in the package. The available files are {file_names} ", sys)
