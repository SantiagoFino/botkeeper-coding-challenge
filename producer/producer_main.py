from reader import CSVReader
from kafka_producer import KafkaMessageProducer
from config import settings
from data_cleaner import clean_data
from common.logger import logger
import time


def main():
    reader = CSVReader(path=settings.CSV_FILE_PATH)
    producer = KafkaMessageProducer(bootstrap_servers=settings.BOOSTRAP_SERVERS,
                                    topic=settings.TOPIC)
    for row in reader.read_csv():
        message = {
            'description': row['dascription'],
            'amount': row['amount']
        }
        cleaned_message = clean_data(message)
        producer.send_message(message=cleaned_message)
        logger.info(message)
        time.sleep(1)
    
if __name__ == "__main__":
    main()