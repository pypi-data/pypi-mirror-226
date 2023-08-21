
class KafkaPublisher:
    def publish_events(self, event):
        for i in range(10):
            print(f'Publishing the event: {event}, progress: {i}/10')
        print("published the event")
        return "SUCCESS"
