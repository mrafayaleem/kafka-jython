from kafkajython.examples import ConsumerGroupExample


def run():
    # List of arguments for initializing the consumer
    args = [
        "localhost:2181",
        "test-group",
        "another-replicated-topic",
        "3"
    ]
    ConsumerGroupExample.main(args)

if __name__ == '__main__':
    run()
