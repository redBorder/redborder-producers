#!/usr/bin/env python3

import json
import time
from kafka import KafkaProducer

FILENAME = "/usr/lib/redborder/producers/json/bit_torrent.json"
KAFKA_BROKER = "localhost:9092"
TOPIC_PREFIX = "rb_event_post_"
NAMESPACE_UUID = "352369f8-60fb-4b72-a603-d1d8393cca0a"

def read_json_file(json_file):
    with open(json_file, "r") as file:
        return [json.loads(line) for line in file]

def replay_messages(json_file, producer):
    messages = read_json_file(json_file)
    
    pre_timestamp = 0
    for message in messages:
        timestamp = message["timestamp"]
        message["timestamp"] = int(time.time())
            
        try:
            producer.send(TOPIC_PREFIX + NAMESPACE_UUID, json.dumps(message).encode("utf-8"))
            producer.flush()
        except Exception as e:
            print(f"Error delivering message: {e}")
            time.sleep(1)
            continue
        print("Delivered message")
        if pre_timestamp > 0:
            next_time = timestamp - pre_timestamp
            print(next_time)
            time.sleep(next_time)
        pre_timestamp = timestamp
    producer.close()

if __name__ == "__main__":
    producer = KafkaProducer(bootstrap_servers=[KAFKA_BROKER])
    replay_messages(FILENAME, producer)
