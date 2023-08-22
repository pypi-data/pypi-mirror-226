from .exception import CustomException
import pandas as pd
import os
import sys
import pkg_resources

class FetchData:
    def __init__(self):
        self.__data_directory = pkg_resources.resource_filename('TestDSPackage', 'Data')

    def load_data(self, file_name: str):
        file_name = file_name.lower() + '.csv'
        self.__file_path = pkg_resources.resource_filename('TestDSPackage', f'Data/{file_name}')
        try:
            df = pd.read_csv(self.__file_path)
            print(f"The file '{file_name}' exists in the '{self.__data_directory}' directory.")
            return df
        except FileNotFoundError:
            files = pkg_resources.resource_listdir('TestDSPackage', 'Data')
            file_names = [item for item in files if item.lower() == file_name]
            raise CustomException(f"The file '{file_name}' does not exist in the package. The available files are {file_names} ", sys)


