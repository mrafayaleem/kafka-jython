##Producer

### 1. Single thread, no replication
##### Topic:
```
bin/kafka-topics.sh --zookeeper 172.31.4.214:2181 --create --topic test-rep-one --partitions 6 --replication-factor 1
```

##### Pure Java
```
java -cp ".:./libs/*" kafkajython.benchmarks.ProducerPerformance --topic test-rep-one --num-records 50000000 --record-size 100 --throughput -1 --producer-props acks=1 bootstrap.servers=172.31.15.249:9092 buffer.memory=67108864 batch.size=8196
```
##### Java interfaced Jython
```
jython -J-cp ".:./libs/*" benchmarks/src/main/jython/java_interfaced_jython_prodcuer.py --topic test-rep-one --throughput -1 --num-records 50000000 --record-size 100 --producer-props acks=1 bootstrap.servers=172.31.15.249:9092 buffer.memory=67108864 batch.size=8196
```
##### Pure Jython
```
jython -J-cp ".:./libs/*" benchmarks/src/main/jython/producer_performance.py --topic test-rep-one --num-records 50000000 --record-size 100 --producer-props acks=1 bootstrap.servers=172.31.15.249:9092 buffer.memory=67108864 batch.size=8196
```
##### Pure Python
```
python benchmarks/src/main/python/producer_performance.py --topic test-rep-one --num-records 50000000 --record-size 100 --producer-props acks=1 bootstrap_servers=172.31.15.249:9092 buffer_memory=67108864 batch_size=8196
```
### 2. Single-thread, async 3x replication
##### Topic
```
bin/kafka-topics.sh --zookeeper 172.31.4.214:2181 --create --topic test-rep-three --partitions 6 --replication-factor 3
```
Commands are the same as in the previous case.

### 3. Single-thread, sync 3x replication
For every command in section 1, change `acks` to `-1` and `batch.size` to `64000`.

