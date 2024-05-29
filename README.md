# Stream of Financial Transactions

In this repository, you will find a Python script that simulates real-time processing of financial transactions, preparing a given dataset for clustering by performing preprocessing steps.

To adress this problem, we utilize [Kafka](https://kafka.apache.org/), an open-source distributed event streaming platform that operates with 2 main components. The **producer** and the **consumer**.

* The **producer** is responsible for reading data from the CSV file, performing the cleaning process on both the description and amount columns, and then sending the data to the Kafka broker for storage.

* The **consumer** is a service that remains active, continuously reading the data as it is loaded by the producer. Additionally, it sends the read data to a posgres database in real time.


## Database configuration

As the records are streamed into a posgreSQL database, its credentials can be modified in `./consumer/config/` in the `DB_SETTINGS` dictionary. If not, the table can be created using docker as follows:

First, pull the official PostgreSQL Docker image

```bash
docker pull posgres
```

If the code is going to be compute using docker containers, you must create a network

```bash
docker network create app-tier --driver bridge
```

Run the PostgreSQL container with the following environment variables

```bash
docker run --name financial-db-container -e POSTGRES_DB=financial-transactions -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=financialdb -p 5433:5432 -d postgres
```

Or if the code is going to run in a container, you must connect to the network you just create

```bash
docker run --name financial-db-container -e POSTGRES_DB=financial-transactions --network app-tier -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=financialdb -p 5433:5432 -d postgres 
```

Now, connect to your PostgreSQL container and create the table for storing messages.

```bash
docker exec -it financial-db-container psql -U admin -d financial-transactions
```

That command will open a sql terminal where you can create the table running:

```sql
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    amount FLOAT NOT NULL,
    description TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Repository Configuration

Clone the repository

```bash
git clone https://github.com/SantiagoFino/stream-financial-transactions.git
```

Load the `.csv` file in the folder `./producer/data`. Preferably, the file name should be *dataset.csv*. Otherwise, its name must be passed in the argument `--csv_name`.

If the code its ggoing to be running in a docker container, please update the consumer settings as follows.

1. Go to `/consumer/config.py` 
2. Change the variable `DB_SETTINGS` for the following value
```python
{
    'dbname': 'financial-transactions',
    'user': 'admin',
    'password': 'financialdb',
    'host': 'financial-db-container',
    'port': 5432 
}
``` 

## Run it locally

For running Kafka locally follow the steps presented in the oficial [Apache Kafka](https://kafka.apache.org/quickstart) web page.

### 1. Install Kafka
[Download](https://www.apache.org/dyn/closer.cgi?path=/kafka/3.7.0/kafka_2.13-3.7.0.tgz) the latest Kafka release and extract it

```bash
$ tar -xzf kafka_2.13-3.7.0.tgz
$ cd kafka_2.13-3.7.0
```

### 2. Start the Kafka enviroment with Zookeeper

Start the Zookeeper service
```bash
$ bin/zookeeper-server-start.sh config/zookeeper.properties
```

Open another terminal and start the Kafka broker service
```bash
$ bin/kafka-server-start.sh config/server.properties
```

### 3. Install the requirements.txt

In two new terminals, install the `requirements.txt` files for both the producer and the consumer.

```bash
$ cd consumer
$ pip install -r requirements.txt
```

```bash
$ cd producer
$ pip install -r requirements.txt
```

Yes, by this moment we are using 5 terminals.

### 4. Activate the consumer

Being in the *consumer* folder, run:

```bash
python3 main.py --bootstrap_services localhost:9092 
```

The `--batch_size` can also be configured. It represents the number of records that can be uploaded to the posgres database

### 5. Run the producer
Being in the *producer* folder, run:

```bash
python3 main.py --bootstrap_services localhost:9092 
```

Other arguments that can be configured are

```bash
--csv_name   --chunk_size   --num_tasks
```

In case the *.csv* file has a different name than *dataset.csv* it must be specified. The `chunk_size` arg represents the number of rows to read from the CSV file at a time. The `num_tasks` arg represents the number of concurrent tasks to run for processing messages in parallel.

*Note: the `--boostrap_services` arg is mandatory when run the consumer/producer locally and should have the value `localhost:9092`*


## Run it in a Container using Docker

An Apache Kafka client instance should run on the same docker network as the client. For this purpose, we follow the steps presented in [Bitnamy](https://hub.docker.com/r/bitnami/kafka).

### 1. Launch the Apache Kafka server instance

This container will be attached to the `app-tier` network defined before

```bash
docker run -d --name kafka-server --hostname kafka-server \
    --network app-tier \
    -e KAFKA_CFG_NODE_ID=0 \
    -e KAFKA_CFG_PROCESS_ROLES=controller,broker \
    -e KAFKA_CFG_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9093 \
    -e KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT \
    -e KAFKA_CFG_CONTROLLER_QUORUM_VOTERS=0@kafka-server:9093 \
    -e KAFKA_CFG_CONTROLLER_LISTENER_NAMES=CONTROLLER \
    bitnami/kafka:latest
```

### 2. Build the docker images

Once the Kafka server is attached to the network, we can create both the consumer and the producer images

```bash
$ cd producer
$ docker build -t producer .
$ cd ..
$ cd consumer
$ docker build -t consumer .
```


### 3. Run the instances

Then run the containers attached to the `app-tier` network. It is important to run the consumer container before the producer one. If not, the data will not be streamed in the correct way.

```bash
docker run -d --name consumer-container --network app-tier consumer
```

```bash
docker run -d --name producer-container --network app-tier producer
```

