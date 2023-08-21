from app.kafka_example import kafka_const
import time
from confluent_kafka import Producer

if __name__ == '__main__':
    # topic = os.environ['CLOUDKARAFKA_TOPIC'].split(",")[0]
    #
    # # Consumer configuration
    # # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    # conf = {
    #     'bootstrap.servers': os.environ['CLOUDKARAFKA_BROKERS'],
    #     'session.timeout.ms': 6000,
    #     'default.topic.config': {'auto.offset.reset': 'smallest'},
    #     'security.protocol': 'SASL_SSL',
    #     'sasl.mechanisms': 'SCRAM-SHA-256',
    #     'sasl.username': os.environ['CLOUDKARAFKA_USERNAME'],
    #     'sasl.password': os.environ['CLOUDKARAFKA_PASSWORD']
    # }

    topic = kafka_const.CLOUDKARAFKA_TOPIC.split(",")[0] # os.environ['CLOUDKARAFKA_TOPIC'].split(",")

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

    p = Producer(**conf)


    def delivery_callback(err, msg):
        if err:
            print('%% Message failed delivery: %s\n' % err)
        else:
            print('%% Message delivered to %s [%d]\n' %
                             (msg.topic(), msg.partition()))

    messages = ["Hello Test click-" + str(i) for i in range(100)]
    for msg in messages:
        try:
            print(f'Publishing message: {msg} on topic: {topic}')
            p.produce(topic, msg.rstrip(), callback=delivery_callback)
            time.sleep(1)
        except BufferError as e:
            print('%% Local producer queue is full (%d messages awaiting delivery): try again\n' %
                             len(p))
        p.poll(0)

    print('%% Waiting for %d deliveries\n' % len(p))
    p.flush()


"""

%4|1659499628.236|CONFWARN|rdkafka#producer-1| [thrd:app]: Configuration property group.id is a consumer property and will be ignored by this producer instance
% Message delivered to vz78igft-click [1]
%4|1659499628.236|CONFWARN|rdkafka#producer-1| [thrd:app]: Configuration property session.timeout.ms is a consumer property and will be ignored by this producer instance
%4|1659499628.236|CONFWARN|rdkafka#producer-1| [thrd:app]: Configuration property auto.offset.reset is a consumer property and will be ignored by this producer instance

"""