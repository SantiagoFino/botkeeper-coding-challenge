from kafka_consumer import KafkaMessageConsumer
from processor import process_in_db
from config import settings
from utils.logger import logger
from utils.errors import KafkaConsumerError


async def run_consumer(args):
    consumer = KafkaMessageConsumer(
        topic=settings.TOPIC,
        bootstrap_servers=args.bootstrap_servers,
        group_id=settings.GROUP_ID,
        batch_size=args.batch_size
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
