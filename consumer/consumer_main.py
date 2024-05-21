from kafka_consumer import KafkaMessageConsumer
from processor import process_in_logfile
from config import settings
import asyncio


async def main():
    consumer = KafkaMessageConsumer(
        topic=settings.TOPIC,
        boostrap_servers=settings.BOOSTRAP_SERVERS,
        group_id=settings.GROUP_ID
    )
    await consumer.consume(
        processor=lambda x: process_in_logfile(message=x)
        )
    
if __name__ == "__main__":
    asyncio.run(main())
