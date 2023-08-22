from fetchdata import FetchData
from exception import CustomException


try:
    fd = FetchData()
    df = fd.load_data('headbrainqw')
    print(df.head())
except CustomException as e:
    print(f"Custom Error: {e}")
