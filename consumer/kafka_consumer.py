from aiokafka import AIOKafkaConsumer
import asyncio
import json
from typing import Callable
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict

from utils.errors import KafkaConsumerError, MessageHandlerError, ConsumerTaskCreationError

class KafkaMessageConsumer:
    def __init__(self, topic: str, bootstrap_servers: str, group_id: str, batch_size: int) -> None:
        """
        Constructor of the Kafka consumer
        Params:
            topic (str):
            bootstrap_servers (str):
            group_id (str):
        """
        self.batch_size = batch_size
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

    async def handle_message(self, messages: List[Dict], processor: Callable):
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
                await loop.run_in_executor(executor, processor, messages)
        except asyncio.CancelledError:
            raise MessageHandlerError(f"Current task has been canceled: {e}")
        except Exception as e:
            raise KafkaConsumerError(f"Unexpected error handling the messages {type(messages)}: {e}")

    async def consume_message(self, processor: Callable):
        """
        Asynchronously consumes messages and creates tasks to handle each message
        Param:
            processor (Callable): function that defines the logic to follow after the extraction
        """
        messages = []
        try:
            async for msg in self.consumer:
                messages.append(msg.value)
                if len(messages) >= self.batch_size:
                    await self.handle_message(messages, processor)
                    messages = []
            # Process any remaining messages
            if messages:
                await self.handle_message(messages, processor)
                
        except asyncio.CancelledError as e:
            raise ConsumerTaskCreationError(f"Current task was canceled: {e}")
        except Exception as e:
            raise KafkaConsumerError(f"Unexpected error creating the message taks: {e}")