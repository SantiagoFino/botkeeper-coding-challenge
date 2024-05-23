from kafka_consumer import KafkaMessageConsumer
from processor import process_in_logfile, process_in_db
from config import settings
import asyncio
from logger import logger
from errors import KafkaConsumerError


async def main():
    consumer = KafkaMessageConsumer(
        topic=settings.TOPIC,
        bootstrap_servers=settings.BOOSTRAP_SERVERS,
        group_id=settings.GROUP_ID,
        batch_size=settings.BATCH_SIZE
    )
    await consumer.start()
    try:
        await consumer.consume_message(processor=process_in_db)
    except KafkaConsumerError as e:
        logger.error(str(e))
    except Exception as e:
        logger.error(f"An unexpected error occurs while consuming the data: {e}")
    finally:
        await consumer.stop()
    
if __name__ == "__main__":
    asyncio.run(main())
