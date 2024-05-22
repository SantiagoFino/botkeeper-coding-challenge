import numpy as np

class AmountCleaner:
    def __init__(self, amount, scaler) -> None:
        self.amount = amount
        self.scaler = scaler
    
    def clean_amount(self) -> float:
        """
        Normalizes the amount using a MinMaxScaler
        Return:
            float between 0 and 1 representing the normalized amount
        """
        self.amount = np.array(self.amount).reshape(-1, 1)
        self.amount = self.scaler.transform(self.amount)[0][0]
        return self.amount