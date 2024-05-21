import joblib
import numpy as np
from logger import logger
from errors import ScalerReaderError, FileNotFound, DataCleanerError       


def load_scaler(scaler_path: str):
    """
    Loads the scaler that will be used in the 'amount' cleaning
    Params:
        scaler-path (str): path where the scaler .pkl file is stored
    Returs:
        sklearn-preprocessor MinMaxScaler object
    Raise:
        FileNotFound in case that the .pkl scaler file does not exists
        ScalerReaderError if any other error occurs when reading the scaler
    """
    try:
        scaler = joblib.load(scaler_path)
        return scaler
    
    except FileNotFoundError:
        logger.error(f"Scaler file {scaler_path} not found")
        raise FileNotFound(f"Scaler file {scaler_path} not found")
    except Exception as e:
        logger.error(f"Error reading the scaler file: {e}")
        raise ScalerReaderError(f"Error reading the scaler file: {e}")


class DataCleaner:
    def __init__(self, row: dict, scaler) -> None:
        """
        Constructor of the DataCleaner class
        Params:
            row (dict): dictionary with the key-value pairs corresponding to the description 
            and the amount of the transaction
            scaler (sklearn preprocessing object): loaded scaler
        """
        self.description = row['description']
        self.amount = row['amount']
        self.scaler = scaler

    def clean_amount(self) -> None:
        """
        Normalizes the 'amount' value based on the class scaler
        """
        self.amount = np.array(self.amount).reshape(-1, 1)
        self.amount = self.scaler.transform(self.amount)[0][0]
        
    def clean_description(self) -> None:
        self.description = self.description.lower()

    def clean_data(self) -> dict:
        try:
            self.clean_amount()
            self.clean_description()

            return {'description': self.description,
                    'amount': self.amount}
        except Exception as e:
            logger.error(f"Unexpected error cleaning either {self.description} or {self.amount}: {e}")
            raise DataCleanerError(f"Unexpected error cleaning either {self.description} or {self.amount}: {e}")