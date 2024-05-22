import pandas as pd
from errors import CSVReaderError, FileNotFound, MissingColumnError


EXPECTED_COLUMNS = ['Description', 'Amount']


class CSVReader:
    def __init__(self, path: str, chunk_size=1000) -> None:
        """
        Constructor of the CSVReader
        Params:
            path (str): path to the .csv file
            chunk_size (int): amount of record read by pandas in each task
        """
        self.path = path
        self.chunk_size = chunk_size

    def read_csv(self):
        """
        Reads a .csv file row by  row from the class path.
        Returns:
            a pd.DataFrame representing a chunk of the .cvs file
        Raise:
            FileNotFound if the .csv path of the class is not found
            MissingColumnError if one of the required columns is not in the csv files
            CSVReaderError if another unexpected error occurs
        """
        try:
            df_iter = pd.read_csv(self.path, chunksize=self.chunk_size)
            # checks the columns in the first chunk
            first_chunk = next(df_iter)
            if not all(column in first_chunk.columns for column in EXPECTED_COLUMNS):
                raise MissingColumnError(f"Missing one of the required columns: {EXPECTED_COLUMNS}")
            yield first_chunk
            yield from df_iter

        except FileNotFoundError:
            raise FileNotFound(f"csv file {self.path} not found")
        except Exception as e:
            raise CSVReaderError(f"Unexpected error while reading {self.path}: {str(e)}")
