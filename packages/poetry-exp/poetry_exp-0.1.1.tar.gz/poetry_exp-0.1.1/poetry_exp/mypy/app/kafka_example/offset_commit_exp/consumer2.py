from confluent_kafka import Consumer
from app.kafka_example import kafka_const


def write_num_to_file(num, file_path="num.db"):
    with open(file_path, "a") as f:
        f.write(str(num))
        f.write('\n')


kafka_config = {
        'bootstrap.servers': kafka_const.CLOUDKARAFKA_BROKERS, #os.environ['CLOUDKARAFKA_BROKERS'],
        'group.id': "%s-consumer" % kafka_const.CLOUDKARAFKA_USERNAME,
        'security.protocol': 'SASL_SSL',
        'sasl.mechanisms': 'SCRAM-SHA-256',
        'sasl.username': kafka_const.CLOUDKARAFKA_USERNAME, #os.environ['CLOUDKARAFKA_USERNAME'],
        'sasl.password': kafka_const.CLOUDKARAFKA_PASSWORD #os.environ['CLOUDKARAFKA_PASSWORD']
    }


c = Consumer(**kafka_config)
topic = "vz78igft-test-offset"
c.subscribe(topics=[topic])
print(f'Consuming messages from topic: {topic}')
while True:
    msg = c.poll(1)
    if msg:
        print(f'Consumed message: {msg.value()},'
              f' key: {msg.key()},'
              f' topic: {msg.topic()}, offset: {msg.offset()}'
              f' partition: {msg.partition()}, ')
        write_num_to_file(msg.value())
        c.commit()

