import joblib
from utils.logger import logger
import pandas as pd
from utils.errors import ScalerReaderError, FileNotFound, DataCleanerError     
from preprocessing.derscription_cleaner import  TextCleaner
from preprocessing.amount_cleaner import AmountCleaner


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
    def __init__(self, scaler) -> None:
        """
        Constructor of the DataCleaner class
        Params:
            scaler (sklearn preprocessing object): loaded scaler
        """
        self.scaler = scaler

    def clean_description(self, description: str) -> None:
        """
        Cleans the description of the financial record
        """
        try:
            text_cleaner = TextCleaner(text=description)
            clean_description = text_cleaner.clean_description()
            return clean_description
        except Exception:
            raise DataCleanerError(f"Error cleaning the description {self.description}")
        
    def clean_amount(self, amount) -> None:
        """
        Normalizes the 'amount' value based on the class scaler
        Params:
            amount (str, int or float): amount for the financial transaction to be cleaned
        Raise:
            DataCleanerError if an error in the cleaning process is found
        """
        try:
            amount_cleaner = AmountCleaner(amount=amount, scaler=self.scaler)
            clean_amount = amount_cleaner.clean_amount()
            return clean_amount
        except Exception:
            raise DataCleanerError(f"Error cleaning the amount {self.amount}")
        
    def clean_row(self, row: dict) -> dict:
        try:
            amount = self.clean_amount(amount=row["Amount"])
            description = self.clean_description(description=row["Description"])
            return {'description': description,
                    'amount': amount}
        except Exception as e:
            logger.error(f"Unexpected error cleaning ocurr while cleaning the record: {e}")
            raise DataCleanerError(f"Unexpected error cleaning ocurr while cleaning the record: {e}")
        
    def clean_chunk(self, chunk: pd.DataFrame) -> pd.DataFrame:
        """
        Cleans a chunk of the data
        """
        cleaned_data = chunk.apply(self.clean_row, axis=1)
        return pd.DataFrame(cleaned_data.tolist())
