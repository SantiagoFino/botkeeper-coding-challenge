class KafkaError(Exception):
    """Base class for other exceptions"""
    pass

class CSVReadError(KafkaError):
    """Raised when there is an error reading the CSV file"""
    pass

class KafkaProduceError(KafkaError):
    """Raised when there is an error producing messages to Kafka"""
    pass
