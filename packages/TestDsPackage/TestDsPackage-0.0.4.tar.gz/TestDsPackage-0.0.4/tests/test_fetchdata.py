from TestDSPackage.fetchdata import FetchData, CustomException

def test_load_existing_data():
    fd = FetchData()
    df = fd.load_data('salaries')
    assert df is not None

def test_load_nonexistent_data():
    fd = FetchData()
    try:
        df = fd.load_data('ss')
    except CustomException as e:
        assert "The file 'ss.csv' does not exist in the package." in str(e)
