class KafkaConsumerError(Exception):
    """Base class for other kafka copnsumer exceptions"""
    pass

class MessageHandlerError(KafkaConsumerError):
    """Raised when a message cannot get handled by the threads"""
    pass

class ConsumerTaskCreationError(KafkaConsumerError):
    """Raised when a pool of messages cannot be enque in a task"""
    pass