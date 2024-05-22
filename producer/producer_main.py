from time import time
import asyncio

from reader import CSVReader
from kafka_producer import KafkaMessageProducer
from config import settings
from preprocessing.data_cleaner import DataCleaner, load_scaler
from errors import FileNotFound, CSVReaderError, KafkaProduceError, DataCleanerError
from logger import logger
    

async def process_chunk(chunk, cleaner, producer):
    """
    Processes a chunk of data, cleaning it and sending each clean row to a Kafka topic
    Params:
        chunk (pd.DataFrame): chunk of data to be processed
        cleaner (DataCleaner): DataCleaner object that will be use to clean the data
        producer (KafkaMessageProducer): Object in charge of sending the message to the topic
    """
    cleaned_chunk = cleaner.clean_chunk(chunk)
    for _, row in cleaned_chunk.iterrows():
        await producer.send_message(message=row.to_dict())


async def main():
    # creates the producer and the cleaner objects and reads the .pkl file where the MinMaxScaler is located
    producer = KafkaMessageProducer(bootstrap_servers=settings.BOOSTRAP_SERVERS,
                                    topic=settings.TOPIC)
    scaler = load_scaler(scaler_path=settings.SCALER_PATH)
    cleaner = DataCleaner(scaler=scaler)
    await producer.start()

    try:
        # creates the reader
        reader = CSVReader(path=settings.CSV_FILE_PATH, chunk_size=settings.CHUNK_SIZE)
        tasks = []
        # iterates over the chunks produced by the reader, creating cleaning tasks to run them asynchronously
        for chunk in reader.read_csv():
            task = asyncio.create_task(process_chunk(chunk=chunk, cleaner=cleaner, producer=producer))
            tasks.append(task)

            # If there are more than n (in this case 5) tasks, compute them
            if len(tasks) >= settings.NUM_TASKS:
                await asyncio.gather(*tasks)
                tasks = []
            
        if tasks:
            await asyncio.gather(*tasks)
            
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