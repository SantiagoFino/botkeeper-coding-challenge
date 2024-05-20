from reader import CSVReader
from kafka_producer import KafkaMessageProducer
from config import settings
from data_cleaner import clean_data
from time import time

def main():
    reader = CSVReader(path=settings.CSV_FILE_PATH)
    producer = KafkaMessageProducer(bootstrap_servers=settings.BOOSTRAP_SERVERS,
                                    topic=settings.TOPIC)
    for row in reader.read_csv():
        message = {
            'description': row['Description'],
            'amount': row['Amount']
        }
        cleaned_message = clean_data(message)
        producer.send_message(message=cleaned_message)

    producer.flush()
    
    
if __name__ == "__main__":
    main()