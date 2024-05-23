import os 

class Settings:
    """
    The settings class is used to store all the configuration values for the application.
    """
    PROJECT_NAME: str = "financial-transactions-streaming"
    TOPIC: str = 'financial_transactions'
    SCALER_PATH: str = os.path.join(os.getcwd(), 'data/scaler.pkl')


settings = Settings()