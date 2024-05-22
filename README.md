# Stream of Financial Transactions

In this repository, you will find a Python script that simulates real-time processing of financial transactions, preparing a given dataset for clustering by performing preprocessing steps.

To adress this problem, we utilize [Kafka](https://kafka.apache.org/), an open-source distributed event streaming platform that operates with 2 main components. The **producer** and the **consumer**.

* The **producer** is responsible for reading data from the CSV file, performing the cleaning process on both the description and amount columns, and then sending the data to the Kafka broker for storage.

* The **consumer** is a service that remains active, continuously reading the data as it is loaded by the producer. Additionally, it sends the read data to a log file in real time.

## Repository Configuration

Clone the repository

```bash
git clone https://github.com/SantiagoFino/stream-financial-transactions.git
```

Load the `.csv` file in the folder `./producer/data`. It should have the name "dataset.csv". Otherwise, the variable called `CSV_FILE_PATH` stored in `./producer/config.py` should be renamed to the one of the csv file.

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



## Run it in a Container using Docker

An Apache Kafka client instance should run on the same docker network as the client. For this purpose, we follow the steps presented in [Bitnamy](https://hub.docker.com/r/bitnami/kafka).

### 1. Create a network

```bash
docker network create app-tier --driver bridge
```

### 2. Launch the Apache Kafka server instance

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

### 3. Build the docker images

Once the Kafka server is attached to the network, we can create both the consumer and the producer images

```bash
$ docker build -t producer
$ docker build -t consumer
```


### 4. Run the instances

Then run the containers attached to the `app-tier` network. It is important to run the consumer container before the producer one. If not, the data will not be streamed in the correct way.

```bash
docker run -d --name consumer-container --network app-tier consumer
```

```bash
docker run -d --name producer-container --network app-tier producer
```

