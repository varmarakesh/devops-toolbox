__author__ = 'rakesh.varma'
from pykafka import KafkaClient
client = KafkaClient(hosts='52.36.118.218:9092')
topic = client.topics['PD']
with topic.get_sync_producer() as producer:
    for i in range(4):
        producer.produce('test message ' + str(i ** 2))
