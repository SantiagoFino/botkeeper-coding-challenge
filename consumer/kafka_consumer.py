from aiokafka import AIOKafkaConsumer
import asyncio
import json
from typing import Callable
from concurrent.futures import ThreadPoolExecutor
from errors import KafkaConsumerError, MessageHandlerError, ConsumerTaskCreationError

class KafkaMessageConsumer:
    def __init__(self, topic: str, bootstrap_servers: str, group_id: str) -> None:
        """
        Constructor of the Kafka consumer
        Params:
            topic (str):
            bootstrap_servers (str):
            group_id (str):
        """
        self.consumer = AIOKafkaConsumer(topic,
                                         bootstrap_servers=bootstrap_servers,
                                         group_id=group_id,
                                         value_deserializer=lambda x: json.loads(x.decode('utf-8')))
    
    async def start(self) -> None:
        """
        Starts the kafka consumer
        """
        await self.consumer.start()

    async def stop(self) -> None:
        """
        Stops the kafka consumer
        """
        await self.consumer.stop()

    async def handle_message(self, message: dict, processor: Callable):
        """
        Offloads the cpu-bounded task to a thread
        Param:
            message (dict)
            processor (Callable): function that defines the logic to follow after the extraction  
        """
        try:
            loop = asyncio.get_event_loop()
            # creates a pool of threads and submits task to each thread
            with ThreadPoolExecutor() as executor:
                await loop.run_in_executor(executor, processor, message)
        except asyncio.CancelledError:
            raise MessageHandlerError(f"Current task has been canceled: {e}")
        except Exception as e:
            raise KafkaConsumerError(f"Unexpected error handling the message {message}")

    async def consume_message(self, processor: Callable):
        """
        Asynchronously consumes messages and creates tasks to handle each message
        Param:
            processor (Callable): function that defines the logic to follow after the extraction
        """
        try:
            async for msg in self.consumer:
                asyncio.create_task(self.handle_message(msg.value, processor))
        except asyncio.CancelledError as e:
            raise ConsumerTaskCreationError(f"Current task was canceled: {e}")
        except Exception as e:
            raise KafkaConsumerError(f"Unexpected error creating the message taks")