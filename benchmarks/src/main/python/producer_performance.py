import traceback
import time
import sys
import argparse

from kafka import KafkaProducer


class ProducerPerformance(object):

    @staticmethod
    def run():
        parser = get_args_parser()
        try:
            parse_result = parser.parse_args()

            topic_name = parse_result.topic
            num_records = parse_result.num_records
            record_size = parse_result.record_size
            producer_props = parse_result.producer_config

            props = {}
            for prop in producer_props:
                k, v = prop.split('=')
                try:
                    v = int(v)
                except ValueError:
                    pass
                props[k] = v

            producer = KafkaProducer(**props)
            record = bytes(bytearray(record_size))
            stats = Stats(num_records, 5000)

            for i in xrange(num_records):
                send_start_ms = get_time_millis()
                future = producer.send(topic=topic_name, value=record)
                future.add_callback(stats.next_completion(
                        send_start_ms, record_size, stats))

            producer.close()
            stats.print_total()
        except Exception as e:
            exc_info = sys.exc_info()
            traceback.print_exception(*exc_info)
            sys.exit(1)


class Stats(object):

    def __init__(self, num_records, reporting_interval):
        self.start = get_time_millis()
        self.window_start = get_time_millis()
        self.index = 0
        self.iteration = 0
        self.sampling = int(num_records / min(num_records, 500000))
        self.latencies = [0] * (int(num_records / self.sampling) + 1)
        self.max_latency = 0
        self.total_latency = 0
        self.window_count = 0
        self.window_max_latency = 0
        self.window_total_latency = 0
        self.window_bytes = 0
        self.count = 0
        self.bytes = 0
        self.reporting_interval = reporting_interval

    def record(self, iter, latency, bytes, time):
        self.count += 1
        self.bytes += bytes
        self.total_latency += latency
        self.max_latency = max(self.max_latency, latency)
        self.window_count += 1
        self.window_bytes += bytes
        self.window_total_latency += latency
        self.window_max_latency = max(self.window_max_latency, latency)
        if iter % self.sampling == 0:
            self.latencies[self.index] = latency
            self.index += 1

        if time - self.window_start >= self.reporting_interval:
            self.print_window()
            self.new_window()

    def next_completion(self, start, bytes, stats):
        cb = PerfCallback(self.iteration, start, bytes, stats).on_completion
        self.iteration += 1
        return cb

    def print_window(self):
        elapsed = get_time_millis() - self.window_start
        recs_per_sec = 1000.0 * self.window_count / float(elapsed)
        mb_per_sec = 1000.0 * self.window_bytes / float(elapsed) / (1024.0 * 1024.0)

        print '{0} records sent, {1} records/sec ({2} MB/sec), {3} ms avg ' \
              'latency, {4} max latency.'.format(
                self.window_count,
                recs_per_sec,
                mb_per_sec,
                self.window_total_latency / float(self.window_count),
                float(self.window_max_latency)
        )

    def new_window(self):
        self.window_start = get_time_millis()
        self.window_count = 0
        self.window_max_latency = 0
        self.window_total_latency = 0
        self.window_bytes = 0

    def print_total(self):
        elapsed = get_time_millis() - self.start
        recs_per_sec = 1000.0 * self.count / float(elapsed)
        mb_per_sec = 1000.0 * self.bytes / float(elapsed) / (1024.0 * 1024.0)
        percs = self.percentiles(
                self.latencies, self.index, [0.5, 0.95, 0.99, 0.999])

        print '{0} records sent, {1} records/sec ({2} MB/sec), {3} ms avg ' \
              'latency, {4} ms max latency, {5} ms 50th, {6} ms 95th, {7} ' \
              'ms 99th, {8} ms 99.9th.'.format(
                self.count,
                recs_per_sec,
                mb_per_sec,
                self.total_latency / float(self.count),
                float(self.max_latency),
                percs[0],
                percs[1],
                percs[2],
                percs[3]
        )

    @staticmethod
    def percentiles(latencies, count, percentiles):
        size = min(count, len(latencies))
        sorted_latencies = latencies[:size].sort()
        values = [1 * len(percentiles)]
        for i in xrange(len(percentiles)):
            index = int(percentiles[i] * size)
            values[i] = sorted_latencies[index]

        return values


class PerfCallback(object):

    def __init__(self, iter, start, bytes, stats):
        self.start = start
        self.stats = stats
        self.iteration = iter
        self.bytes = bytes

    def on_completion(self, metadata):
        now = get_time_millis()
        latency = int(now - self.start)
        self.stats.record(self.iteration, latency, self.bytes, now)


def get_time_millis():
    return time.time() * 1000


def get_args_parser():
    parser = argparse.ArgumentParser(
            description='This tool is used to verify the producer performance.')

    parser.add_argument(
            '--topic', type=str,
            help='number of messages to produce',
            required=True,
            action='store',
            metavar='TOPIC',
    )
    parser.add_argument(
            '--num-records', type=long,
            help='Port number',
            required=True,
            action='store',
            metavar='NUM-RECORDS',
            dest='num_records'
    )
    parser.add_argument(
            '--record-size', type=int,
            help='message size in bytes',
            required=True,
            action='store',
            metavar='RECORD-SIZE',
            dest='record_size'
    )
    parser.add_argument(
            '--producer-props', type=str,
            help='kafka producer related configuaration properties like '
                 'bootstrap_servers,client_id etc..',
            required=True,
            nargs='+',
            metavar='PROP-NAME=PROP-VALUE',
            dest='producer_config'
    )

    return parser


if __name__ == '__main__':
    ProducerPerformance.run()
