from confluent_kafka import Producer
from app.kafka_example import kafka_const
import json
import time

kafka_config = {
        'bootstrap.servers': kafka_const.CLOUDKARAFKA_BROKERS, #os.environ['CLOUDKARAFKA_BROKERS'],
        'security.protocol': 'SASL_SSL',
        'sasl.mechanisms': 'SCRAM-SHA-256',
        'sasl.username': kafka_const.CLOUDKARAFKA_USERNAME, #os.environ['CLOUDKARAFKA_USERNAME'],
        'sasl.password': kafka_const.CLOUDKARAFKA_PASSWORD #os.environ['CLOUDKARAFKA_PASSWORD']
    }


def delivery_callback(err, msg):
    if err:
        print('%% Message failed delivery: %s\n' % err)
    else:
        print(f'Message: {msg.value()} delivered to topic: {msg.topic()}')


p = Producer(**kafka_config)

topic = "vz78igft-test-offset"

print(f'Publishing messages to topic: messages from topics: {topic}')

for num in range(100):
    p.produce(topic=topic, value=json.dumps({"number": num}), callback=delivery_callback)
    time.sleep(1)
    p.poll(1)
    p.flush()