# kafka-jython

Note: This repo complements the blog post on [Interfacing Jython with Kafka 0.8.x](http://mrafayaleem.com/2016/03/19/interfacing-jython-with-kafka/). It can also be used as a bare minimum to interface Kafka with Jython.

## Setup

You need to have the following installed on your system.

* Java SDK
* Python
* `virtualenv` and `virtualenvwrapper`
* Kafka 0.9.x or Kafka 0.8.x (assuming you know how to setup and run Kafka)

This is a bare-bones repositiory for working with this [tutorial](https://github.com/mrafayaleem/kafka-jython/). To keep things at a minimum, `Kafka 0.9.1` binaries and `Jython 2.7.0` installer  are included within this repo. This means that you can directly run Kafa and Zookeeper after cloning this.

#### Setting up a virtualenv for Jython
Jython is fully compatible with `virtualenv` and tools such as `pip` and setting a virtualenv with Jython as the interpretter is pretty straightforward.

Jython can be installed using the GUI or console. For GUI, execute the jar and follow the steps. For installing it via console, you can use the following command to start with:

```shell
java -jar jython_installer-2.7.0.jar --console
```
Make a note of the location where you have installed Jython.

`cd` into the directory where you cloned the repo and create a virtualenv using Jython as your interpretter by using the following:

```shell
mkvirtualenv -p /jython-installation-path/jython2.7.0/bin/jython -a kafka-jython kafka-jython
```
You should be in the repo directory right now with your `virtualenv` already activated.

The project layout is as follows:

```
.
├── bin
│   └── windows
├── build
├── config
├── examples
│   └── src
│       └── main
│           ├── java
│           │   └── kafkajython
│           └── python
│               └── consumers
├── libs
└── requirements
```
* **bin:** Contains helper scripts from Kafka and other binaries.
* **build:** This is where your compiled files would go.
* **config:** Various kafka configs.
* **examples:** Jython and Java code for this tutorial.
* **libs:** Kafka jars which we will use as dependencies.
* **requirements:** Python library dependencies.

#### Installing Python dependencies

Once in the repo directory, install all Python dependencies using:

```shell
pip install -r requirements/development.txt
```

#### Compiling source code

Since one of our examples depends on calling Java class directly from Jython, we need to compile it first using:

```shell
javac -cp ".:/your-directory/kafka-jython/libs/*" -d build examples/src/main/java/kafkajython/Consumer*
```

We tell java compiler to include all the dependencies in the `lib` directory while compiling and put the compiled files in the build directory.

#### Running the examples:

To execute the "high level" Java example using Jython:

```shell
jython -J-cp "/your-directory/Projects/kafka-jython/libs/*:/your-directory/Projects/kafka-jython/build:." examples/src/main/python/java_interfaced_jython_consumer.py
```

To execute the pure Jython implementation of the coordinated consumer example, do:

```shell
jython -J-cp "/Users/rafay/Projects/kafka-jython/libs/*" examples/src/main/python/pure_jython_consumer.py
```

## License:

Apache License Version 2.0

## Reporting Bugs:

Please email any bugs or feature requests at: mrafayaleem[at]gmail.com

## Author:

[Mohammad Rafay Aleem](http://mrafayaleem.com/)
