import sys

from kafkajython.benchmarks import ProducerPerformance


def run():
    ProducerPerformance.main(sys.argv[1:])

if __name__ == '__main__':
    run()
