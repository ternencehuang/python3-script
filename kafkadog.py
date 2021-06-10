#! /usr/bin/python3
"""
kafka util
python3 kafkadog.py product -t ternence -m test
python3 kafkadog.py consume -t ternence

@Author: Ternence <xyancywong@outlook.com>
@Time: 2021/6/10 15:14
"""
import argparse
from kafka import KafkaProducer, KafkaConsumer

parser = argparse.ArgumentParser()
parser.add_argument("mode", help="consume of product")
parser.add_argument("-s", "--servers", default="localhost:9092", help="kafka servers address")
parser.add_argument("-t", "--topic", default="", help="kafka topic")
parser.add_argument("-m", "--message", default="", help="message send")
args = parser.parse_args()


if args.topic == "":
    print("\u001b[1;91mtopic cannot be null\u001b[0m")
    exit(1)


def consume():
    consumer = KafkaConsumer(args.topic, bootstrap_servers=args.servers)
    for msg in consumer:
        print(msg)


def produce():
    if args.message == "":
        print("\u001b[1;91mno message send\u001b[0m")
        exit(1)
    producer = KafkaProducer(bootstrap_servers=args.servers)
    producer.send(args.topic, args.message.encode(encoding="utf-8"))


if args.mode == "consume":
    consume()
elif args.mode == "product":
    produce()
else:
    print("\u001b[1;91millegal mode\u001b[0m")
    exit(1)

