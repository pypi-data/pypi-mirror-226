import sys
import os
import time
from app.kafka_example import kafka_const
from confluent_kafka import Consumer, KafkaException, KafkaError


if __name__ == '__main__':
    topics = kafka_const.CLOUDKARAFKA_TOPIC.split(",") # os.environ['CLOUDKARAFKA_TOPIC'].split(",")

    # Consumer configuration
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    conf = {
        'bootstrap.servers': kafka_const.CLOUDKARAFKA_BROKERS, #os.environ['CLOUDKARAFKA_BROKERS'],
        'group.id': "%s-consumer" % kafka_const.CLOUDKARAFKA_USERNAME, #os.environ['CLOUDKARAFKA_USERNAME'],
        'session.timeout.ms': 6000,
        'default.topic.config': {'auto.offset.reset': 'smallest'},
        'security.protocol': 'SASL_SSL',
        'sasl.mechanisms': 'SCRAM-SHA-256',
        'sasl.username': kafka_const.CLOUDKARAFKA_USERNAME, #os.environ['CLOUDKARAFKA_USERNAME'],
        'sasl.password': kafka_const.CLOUDKARAFKA_PASSWORD #os.environ['CLOUDKARAFKA_PASSWORD']
    }

    c = Consumer(**conf)
    c.subscribe(topics)
    print(f'Consuming messages from topics: {topics}')
    try:
        while True:
            msg = c.poll(timeout=5.0)  #c.poll(timeout=1.0)
            print(f'Received message: {msg}')
            if msg is None:
                continue
            if msg.error():
                # Error or event
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    # Error
                    raise KafkaException(msg.error())
            else:
                # Proper message
                print('%% %s [%d] at offset %d with key %s:\n' %
                                 (msg.topic(), msg.partition(), msg.offset(),
                                  str(msg.key())))
                print(msg.value())

    except KeyboardInterrupt:
        print('%% Aborted by user\n')

    # Close down consumer to commit final offsets.
    c.close()


"""
Consuming messages from topics: ['vz78igft-click', 'vz78igft-upload']
Received message: None
Received message: None
Received message: <cimpl.Message object at 0x055F5D40>
% vz78igft-click [1] at offset 0 with key None:

b'Hello Test click1'
Received message: None

"""