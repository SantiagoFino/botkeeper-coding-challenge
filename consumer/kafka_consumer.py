from aiokafka import AIOKafkaConsumer
import asyncio
import json
from typing import Callable


class KafkaMessageConsumer:
    def __init__(self, topic: str, boostrap_servers: str, group_id: str) -> None:
        self.topic = topic
        self.bootstrap_servers = boostrap_servers
        self.group_id = group_id

    async def consume(self, processor: Callable):
        """
        Documentation
        """
        consumer = AIOKafkaConsumer(self.topic,
                                    bootstrap_servers=self.bootstrap_servers,
                                    group_id=self.group_id,
                                    value_deserializer=lambda x: json.loads(x.decode('utf-8')))
        await consumer.start()
        try:
            async for msg in consumer:
                await processor(msg.value)
        finally:
            consumer.stop()
        