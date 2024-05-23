import asyncio
import os

from reader import CSVReader
from kafka_producer import KafkaMessageProducer
from config import settings
from preprocessing.data_cleaner import DataCleaner, load_scaler
from utils.errors import FileNotFound, CSVReaderError, KafkaProduceError, DataCleanerError
from utils.logger import logger
    

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


async def run_producer(args):
    # creates the producer and the cleaner objects and reads the .pkl file where the MinMaxScaler is located
    producer = KafkaMessageProducer(bootstrap_servers=args.bootstrap_servers,
                                    topic=settings.TOPIC)
    scaler = load_scaler(scaler_path=settings.SCALER_PATH)
    cleaner = DataCleaner(scaler=scaler)
    await producer.start()

    try:
        # creates the reader
        reader = CSVReader(path=os.path.join(os.getcwd(), f'data/{args.csv_name}'), 
                           chunk_size=args.chunk_size)
        tasks = []
        # iterates over the chunks produced by the reader, creating cleaning tasks to run them asynchronously
        for chunk in reader.read_csv():
            task = asyncio.create_task(process_chunk(chunk=chunk, cleaner=cleaner, producer=producer))
            tasks.append(task)

            # If there are more than n tasks, compute them
            if len(tasks) >= args.num_tasks:
                await asyncio.gather(*tasks)
                tasks = []
            
        if tasks:
            await asyncio.gather(*tasks)
            
    except (FileNotFound, CSVReaderError, KafkaProduceError, DataCleanerError) as e:
        logger.error(f"Error {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected Error: {str(e)}")
    finally:
        await producer.stop()
