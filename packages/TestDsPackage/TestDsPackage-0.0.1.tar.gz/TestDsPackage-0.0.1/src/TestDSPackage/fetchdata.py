from exception import CustomException
import sys
import pandas as pd
import os

class FetchData:
    def __init__(self) -> None:
        self.__data_directory = "Data"  # Directory where CSV files are stored
    
    def load_data(self, file_name: str):
        file_name = file_name.lower() + '.csv'
        self.__file_path = os.path.join(self.__data_directory, file_name)
        try:
            df = pd.read_csv(self.__file_path)
            print(f"The file '{file_name}' exists in the '{self.__data_directory}' directory.") 
            return df
        except FileNotFoundError as e:
            files = os.listdir(self.__data_directory)
            file_names = [item for item in files if os.path.isfile(os.path.join(self.__data_directory, item))]
            raise CustomException(f"The file '{file_name}' does not exist in the package. The available files are {file_names} ", sys) 
