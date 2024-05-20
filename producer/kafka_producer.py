from kafka import KafkaProducer
import json


class KafkaMessageProducer:
    def __init__(self, bootstrap_servers: str, topic: str):
        self.producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                                      value_serializer=None)
        self.topic = topic


    def send_message(self, message: dict):
        """
        Documentation
        """
        self.producer.send(self.topic,
                           message)
        self.producer.flush()
        