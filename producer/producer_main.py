from reader import CSVReader
from kafka_producer import KafkaMessageProducer
from config import settings
from preprocessing.data_cleaner import DataCleaner, load_scaler
from time import time
from errors import FileNotFound, CSVReaderError, KafkaProduceError, DataCleanerError
from logger import logger
import asyncio
import os

async def main():
    reader = CSVReader(path=os.path.join(os.getcwd(), settings.CSV_FILE_PATH))
    producer = KafkaMessageProducer(bootstrap_servers=settings.BOOSTRAP_SERVERS,
                                    topic=settings.TOPIC)
    scaler = load_scaler(scaler_path=os.path.join(os.getcwd(), settings.SCALER_PATH))
    await producer.start()
    try:
        async for row in reader.read_csv():
            message = {
                'description': row['Description'],
                'amount': row['Amount']
            }
            cleaner = DataCleaner(row=message, scaler=scaler)
            cleaned_message = cleaner.clean_data()
            await producer.send_message(message=cleaned_message)
    except (FileNotFound, CSVReaderError, KafkaProduceError, DataCleanerError) as e:
        logger.error(f"Error {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected Error: {e}")
    finally:
        await producer.stop()
    

if __name__ == "__main__":
    start = time()
    asyncio.run(main())
    print('--- %s seconds ---' %(time() - start))