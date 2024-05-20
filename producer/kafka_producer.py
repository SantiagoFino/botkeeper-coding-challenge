from kafka import KafkaProducer
import json
from logger import logger


class KafkaMessageProducer:
    def __init__(self, bootstrap_servers: str, topic: str) -> None:
        self.producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                                      value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        self.topic = topic

    def send_message(self, message):
        """
        Documentation
        """
        future = self.producer.send(self.topic, message)
        future.add_callback(self.on_send_success)
        future.add_errback(self.on_send_error)

    def on_send_success(self, record_metadata):
        """
        Documentation
        """
        logger.info(f"Message sent to {record_metadata.topic} partition {record_metadata.partition} offset {record_metadata.offset}")

    def on_send_error(self, excp):
        """
        Documentation
        """
        logger.error(f"Failed to send message: {excp}")

    def flush(self):
        self.producer.flush()
        