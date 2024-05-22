from kafka_consumer import KafkaMessageConsumer
from processor import process_in_logfile
from config import settings
import asyncio
from logger import logger
from errors import KafkaConsumerError


async def main():
    consumer = KafkaMessageConsumer(
        topic=settings.TOPIC,
        bootstrap_servers=settings.BOOSTRAP_SERVERS,
        group_id=settings.GROUP_ID
    )
    await consumer.start()
    try:
        await consumer.consume_message(processor=lambda x: process_in_logfile(message=x))
    except KafkaConsumerError as e:
        logger.error(str(e))
    except Exception as e:
        logger.error(f"An unexpected error occurs while consuming the data: {e}")
    finally:
        await consumer.stop()
    
if __name__ == "__main__":
    asyncio.run(main())
