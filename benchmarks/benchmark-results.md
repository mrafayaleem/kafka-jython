# 1. Single thread, no replication
##Pure Java
50000000 records sent, 747417.671943 records/sec (71.28 MB/sec), 429.34 ms avg latency, 2828.00 ms max latency, 265 ms 50th, 1251 ms 95th, 1817 ms 99th, 2497 ms 99.9th.

## Java interfaced Jython
50000000 records sent, 753046.071359 records/sec (71.82 MB/sec), 310.54 ms avg latency, 2189.00 ms max latency, 1 ms 50th, 1416 ms 95th, 1798 ms 99th, 2079 ms 99.9th.

## Pure Jython
50000000 records sent, 117115.217951 records/sec (11.1689775421 MB/sec), 53.95983326 ms avg latency, 4088.0 ms max latency, 2 ms 50th, 328 ms 95th, 1108 ms 99th, 3262 ms 99.9th.

## Pure Python
50000000 records sent, 9707.5761892 records/sec (0.92578660862 MB/sec), 25.82151426 ms avg latency, 1334.0 ms max latency, 26 ms 50th, 44 ms 95th, 54 ms 99th, 226 ms 99.9th.

---
# 2. Single thread, async 3x replication

## Pure Java
50000000 records sent, 427051.126561 records/sec (40.73 MB/sec), 1160.60 ms avg latency, 7428.00 ms max latency, 459 ms 50th, 4282 ms 95th, 6288 ms 99th, 7266 ms 99.9th.

## Java interfaced Jython
50000000 records sent, 446791.589595 records/sec (42.61 MB/sec), 1032.90 ms avg latency, 5925.00 ms max latency, 219 ms 50th, 4602 ms 95th, 5595 ms 99th, 5852 ms 99.9th.

## Pure Jython
50000000 records sent, 118026.409589 records/sec (11.2558755483 MB/sec), 231.39137682 ms avg latency, 5179.0 ms max latency, 6 ms 50th, 982 ms 95th, 1983 ms 99th, 4590 ms 99.9th.

## Pure Python
50000000 records sent, 9845.42251444 records/sec (0.938932658619 MB/sec), 26.58918002 ms avg latency, 1138.0 ms max latency, 25 ms 50th, 44 ms 95th, 59 ms 99th, 539 ms 99.9th.

---
# 3. Single thread, sync 3x relication
## Pure Java
```
java -cp ".:./libs/*" kafkajython.benchmarks.ProducerPerformance --topic test-rep-three --num-records 50000000 --record-size 100 --throughput -1 --producer-props acks=-1 bootstrap.servers=172.31.15.249:9092 buffer.memory=67108864 batch.size=64000
```

50000000 records sent, 205475.511429 records/sec (19.60 MB/sec), 2502.79 ms avg latency, 11165.00 ms max latency, 1769 ms 50th, 6741 ms 95th, 9492 ms 99th, 10640 ms 99.9th.

## Java interfaced Jython
```
jython -J-cp ".:./libs/*" benchmarks/src/main/jython/java_interfaced_jython_prodcuer.py --topic test-rep-three --throughput -1 --num-records 50000000 --record-size 100 --producer-props acks=-1 bootstrap.servers=172.31.15.249:9092 buffer.memory=67108864 batch.size=64000
```

50000000 records sent, 192588.426976 records/sec (18.37 MB/sec), 2659.39 ms avg latency, 19267.00 ms max latency, 751 ms 50th, 9236 ms 95th, 14518 ms 99th, 18843 ms 99.9th.

## Pure Jython
```
jython -J-cp ".:./libs/*" benchmarks/src/main/jython/producer_performance.py --topic test-rep-three --num-records 50000000 --record-size 100 --producer-props acks=-1 bootstrap.servers=172.31.15.249:9092 buffer.memory=67108864 batch.size=64000
```

50000000 records sent, 110700.535126 records/sec (10.5572257162 MB/sec), 1220.20796466 ms avg latency, 7115.0 ms max latency, 861 ms 50th, 4770 ms 95th, 6052 ms 99th, 6747 ms 99.9th.

## Pure Python
```
python benchmarks/src/main/python/producer_performance.py --topic test-rep-three --num-records 50000000 --record-size 100 --producer-props acks=-1 bootstrap_servers=172.31.15.249:9092 buffer_memory=67108864 batch_size=64000
```

49999231 records sent, 9844.45746764 records/sec (0.938840624584 MB/sec), 39.2650510365 ms avg latency, 2359.0 ms max latency, 28 ms 50th, 57 ms 95th, 452 ms 99th, 1108 ms 99.9th.

---
