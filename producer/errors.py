
class FileNotFound(Exception):
    """Raised when there is an error reading a file"""
    pass



class CSVReaderError(Exception):
    """Base class for other exceptions"""
    pass

class MissingColumnError(CSVReaderError):
    """Raise when expected columns are missing in the csv"""
    pass



class KafkaProduceError(Exception):
    """Raised when there is an error producing messages to Kafka"""
    pass



class DataCleanerError(Exception):
    """Raised when an error appears in the datacleaning process"""
    pass

class ScalerReaderError(DataCleanerError):
    """Raised when the scaler cannot be read"""
    pass