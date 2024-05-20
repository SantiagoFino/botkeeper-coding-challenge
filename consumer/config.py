class Settings:
    """
    The settings class is used to store all the configuration values for the application.
    """
    PROJECT_NAME: str = "financial-transactions-streaming"
    TOPIC: str = 'financial_transactions'
    BOOSTRAP_SERVERS: str = 'localhost:9092'
    GROUP_ID: str = 'test_consumer'


settings = Settings()