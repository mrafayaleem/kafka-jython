from concurrent.futures import ThreadPoolExecutor

from java.util import Properties
from java.util import HashMap
from java.lang import String

from kafka.consumer import ConsumerConfig
from kafka.consumer import Consumer


class HighLevelConsumer(object):

    def __init__(self, zookeeper, group_id, topic, thread_count=1, callback=lambda x, y: (x, y)):
        self.consumer = Consumer.createJavaConsumerConnector(
            self._create_consumer_config(zookeeper, group_id)
        )
        self.topic = topic
        self.thread_count = thread_count
        self.callback = callback

    def consume(self):
        topic_count_map = HashMap()
        topic_count_map.put(self.topic, self.thread_count)
        consumer_map = self.consumer.createMessageStreams(topic_count_map)
        streams = consumer_map.get(self.topic)

        with ThreadPoolExecutor(max_workers=self.thread_count) as executor:
            futures = []
            for i, stream in enumerate(streams):
                futures.append(executor.submit(self._decorate(self.callback, i, stream)))

            for future in futures:
                future.result()

    @staticmethod
    def _decorate(callback, thread, stream):
        def decorated():
            it = stream.iterator()
            while it.hasNext():
                callback(thread, String(it.next().message()))

        return decorated

    @staticmethod
    def _create_consumer_config(zookeeper, group_id):
        props = Properties()
        props.put("zookeeper.connect", zookeeper)
        props.put("group.id", group_id)
        props.put("zookeeper.session.timeout.ms", "400")
        props.put("zookeeper.sync.time.ms", "200")
        props.put("auto.commit.interval.ms", "1000")

        return ConsumerConfig(props)
