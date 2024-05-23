class Settings:
    """
    The settings class is used to store all the configuration values for the application.
    """
    PROJECT_NAME: str = "financial-transactions-streaming"
    TOPIC: str = 'financial_transactions'
    GROUP_ID: str = 'test_consumer'
    DB_SETTINGS: dict = {
        'dbname': 'financial-transactions',
        'user': 'admin',
        'password': 'financialdb',
        'host': 'localhost',
        'port': 5433 
        }


settings = Settings()