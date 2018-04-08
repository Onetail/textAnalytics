'''
Kafka topics tool for checking message
'''

from pykafka import KafkaClient
client = KafkaClient(hosts="127.0.0.1:9092")

def listener(subject):
    articleStack = [] 
    topic = client.topics[subject]
    consumer = topic.get_simple_consumer(reset_offset_on_start=True)
    for message in consumer:
        if message is not None:
            print(message.offset, (message.value).decode('utf-8'))
            articleStack.append((message.value).decode('utf-8'))
    return articleStack

if __name__ == '__main__':
    #listener(b'entertainment')
    listener(b'politics')
