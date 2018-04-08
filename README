# Text Analytics System

## Basic Environment 
* System: Ubuntu 16.04.4 LTS
* Python: 3.5.2
* Kafka: 2.11-0.11.0.2
* Internet: Alibaba Cloud (on Great Firewall)

## Flow
* Install Kafka refer to [How to setup Kafka on Ubuntu 16.04](https://hevodata.com/blog/how-to-set-up-kafka-on-ubuntu-16-04/) 
* Create topics in kafka/bin 
```
sudo ./kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic topicName
```   
* Write the python web crawlers with [pykafka](https://github.com/Parsely/pykafka) 
* Build [TF-IDF](https://www.jianshu.com/p/edf666d3995f) Model for each article 
* pipe to the python text analytics  


## Usage

* get the latest news from politics/entertainment 
```
python3 crawler.py politics 
python3 crawler.py entertainment
```   
* get Message from kafka 
```
python3 mqtool.py 
```
* Analytics Message 
```
python3 nlp.py politics 
python3 nlp.py entertainment
```
* Auto crontab 
```
$crontab -e
```
