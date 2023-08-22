import pandas as pd
import importlib.resources as resources
import os
import sys
from .exception import CustomException

class FetchData:
    def __init__(self):
        self.__data_directory = os.path.join(os.path.dirname(__file__), "Data")

    def load_data(self, file_name: str):
        file_name = file_name.lower() + '.csv'
        self.__file_path = os.path.join(self.__data_directory, file_name)
        try:
            df = pd.read_csv(self.__file_path)
            return df
        except FileNotFoundError:
            files = os.listdir(self.__data_directory)
            file_names = [item for item in files if os.path.isfile(os.path.join(self.__data_directory, item))]
            raise CustomException(f"The file '{file_name}' does not exist in the package. The available files are {file_names} ", sys)
