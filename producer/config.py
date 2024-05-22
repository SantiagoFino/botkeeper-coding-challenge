import os 

class Settings:
    """
    The settings class is used to store all the configuration values for the application.
    """
    PROJECT_NAME: str = "financial-transactions-streaming"
    TOPIC: str = 'financial_transactions'
    BOOSTRAP_SERVERS: str = 'kafka-server:9092'
    CSV_FILE_PATH: str = os.path.join(os.getcwd(), 'data/dataset.csv')
    SCALER_PATH: str = os.path.join(os.getcwd(), 'data/scaler.pkl')
    CHUNK_SIZE: int = 1000
    NUM_TASKS: int = 5


settings = Settings()