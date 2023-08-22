import pandas as pd
import importlib.resources as resources
import os
import sys
from .exception import CustomException

class FetchData:
    def __init__(self) -> None:
        self.__data_directory = "Data"  # Directory where CSV files are stored
    
    def load_data(self, file_name: str):
        file_name = file_name.lower() + '.csv'
        try:
            with resources.path('TestDSPackage', os.path.join(self.__data_directory, file_name)) as data_path:
                df = pd.read_csv(data_path)
                print(f"The file '{file_name}' exists in the '{self.__data_directory}' directory.") 
                return df
        except FileNotFoundError:
            files = resources.contents('TestDSPackage.' + self.__data_directory)
            file_names = [item for item in files if item.endswith('.csv')]
            raise CustomException(f"The file '{file_name}' does not exist in the package. The available files are {file_names} ", sys)
