from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaTimeoutError
import json
from utils.errors import KafkaProduceError
from utils.logger import logger


class KafkaMessageProducer:
    def __init__(self, bootstrap_servers: str, topic: str) -> None:
        """
        Constructor of the message producer
        Params:
            bootstrap_servers (str):
            topic (str):
        """
        self.producer = AIOKafkaProducer(bootstrap_servers=bootstrap_servers,
                                         enable_idempotence=True,
                                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        self.topic = topic

    async def start(self) -> None:
        """
        Starts the Kafka producer
        """
        if self.producer:
            await self.producer.start()

    async def stop(self) -> None:
        """
        Stops the Kafka Producer
        """
        await self.producer.stop()

    async def send_message(self, message: dict) -> None:
        """
        Sends a message to the kafka topic
        Param:
            message (dict): key-value pairs corresponding to the description and the
            amount of a transaction
        Raise:
            KafkaProduceError if any error is found in the current messaje sending
        """
        try:
            await self.producer.send_and_wait(self.topic, message)
        except KafkaTimeoutError as e:
            logger.error(f"Error sending message {message}: {e}")
            raise KafkaProduceError(f"Error sending message: {e}")

        