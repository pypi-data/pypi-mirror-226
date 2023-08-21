from app.unittest_exp.src.publisher import KafkaPublisher


def create_backup(bkp_details):
    producer = KafkaPublisher()
    print(f'Creating the backup: {bkp_details}')
    publish_result = producer.publish_events(bkp_details)
    print(f'Created the backup, publish_result: {publish_result}')