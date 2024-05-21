import csv
from errors import CSVReaderError, FileNotFound, MissingColumnError


EXPECTED_COLUMNS = ['Description', 'Amount']


class CSVReader:
    def __init__(self, path: str) -> None:
        """
        Constructor of the CSVReader
        Params:
            path (str): path to the .csv file
        """
        self.path = path

    async def read_csv(self):
        """
        Reads a .csv file row by  row from the class path.
        Yields:
            a dictionary representing a row of the .cvs file
        Raise:
            FileNotFound if the .csv path of the class is not found
            MissingColumnError if one of the required columns is not in the csv files
            CSVReaderError if another unexpected error occurs
        """
        try:
            with open(self.path, mode='r') as f:
                reader = csv.DictReader(f)
                if not all(column in reader.fieldnames for column in EXPECTED_COLUMNS):
                    raise MissingColumnError("Missing expected columns in the given CSV file")
                for row in reader:
                    yield row
        except FileNotFoundError:
            raise FileNotFound(f"csv file {self.path} not found")
        except Exception as e:
            raise CSVReaderError(f"Unexpected error while reading {self.path}: {str(e)}")
