import argparse
import asyncio
from producer_runner import run_producer

async def main(args):
    await run_producer(args)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kafka Consumer with PostgreSQL integration")
    parser.add_argument('--bootstrap_servers', type=str, default='kafka-server:9092', help="Kafka bootstrap servers")
    parser.add_argument('--csv_name', type=str, default='dataset.csv', help="Name of the csv file where the data is stored")
    parser.add_argument('--chunk_size', type=int, default=1000, help="Number of rows to read from the CSV file at a time")
    parser.add_argument('--num_tasks', type=int, default=5, help="Number of concurrent tasks to run for processing messages in parallel")

    args = parser.parse_args()

    asyncio.run(main(args))
