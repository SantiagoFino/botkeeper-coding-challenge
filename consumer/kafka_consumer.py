from kafka import KafkaConsumer
import json
from typing import Callable


class KafkaMessageConsumer:
    def __init__(self, boostrap_servers: str, topic: str, group_id: str) -> None:
        self.consumer = KafkaConsumer(
            topics=topic,
            bootstrap_servers=boostrap_servers,
            group_id=group_id,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

    def consume_message(self, processor: Callable):
        """
        Documentation
        """
        for m in self.consumer:
            processor(m)
        