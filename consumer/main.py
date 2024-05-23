import argparse
import asyncio
from consumer_runner import run_consumer


async def main(args):
    await run_consumer(args)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kafka Consumer with PostgreSQL integration")
    parser.add_argument('--bootstrap_servers', type=str, default='kafka-server:9092', help="Kafka bootstrap servers")
    parser.add_argument('--batch_size', type=int, default=100, help="Number of rows to read from the CSV file at a time")

    args = parser.parse_args()

    asyncio.run(main(args))
