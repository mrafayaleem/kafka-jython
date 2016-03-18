from consumers.group import HighLevelConsumer


def process_message(thread, message):
    print str(thread) + ': ' + str(message)


def run():
    consumer = HighLevelConsumer(
            'localhost:2181', 'unknown', 'another-replicated-topic', 3, callback=process_message)
    consumer.consume()

if __name__ == '__main__':
    run()
