class KafkaError(Exception):
    """Base class for other kafka exceptions"""
    pass

class CSVReadError(KafkaError):
    """Raised when there is an error reading the CSV file"""
    pass

class KafkaConsumeError(KafkaError):
    """Raised when there is an error producing messages to Kafka"""
    pass