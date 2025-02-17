#!/usr/bin/env python3

import json
import time
import argparse
from kafka import KafkaProducer

FILENAME = "/usr/lib/redborder/producers/json/bit_torrent_event.in.json"
TOPIC_PREFIX = "rb_event"

topic = TOPIC_PREFIX

def read_json_file(json_file):
    with open(json_file, "r") as file:
        return [json.loads(line) for line in file]

def rewrite_mimanager(message):
    # message["field"] = "value"
    message["sensor_uuid"] = "656a330c-bbf5-4d77-b1d9-36336e716ef0"
    message["service_provider_uuid"] = "a5e09122-bf39-453a-88e8-4c800b96f199"
    message["namespace_uuid"] = "4331f4b4-abf6-47d8-9def-0a362ab1c716"
    message["organization_uuid"] = "4fe14138-65c5-4a16-a769-1901b0286b83"
    message["building_uuid"] = "59d8a1d8-e05e-48ea-8c7b-fdb3d698a0e1"    
    return message

# Replay messages from a JSON file at the same speed of the original timestamp suggets-
# Alternatively, the speed can be increased by a factor
def replay_messages(json_file, producer, speed_up_factor=1):
    messages = read_json_file(json_file)
    print("ETA (seconds):")
    eta = messages[-1]['timestamp'] - messages[0]["timestamp"]
    eta = eta / speed_up_factor
    print(eta)
    
    pre_timestamp = 0
    for message in messages:
        message = rewrite_mimanager(message)
        timestamp = message["timestamp"]
        message["timestamp"] = int(time.time())
            
        try:
            producer.send(topic, json.dumps(message).encode("utf-8"))
            producer.flush()
        except Exception as e:
            print(f"Error delivering message: {e}")
            time.sleep(1)
            continue
        print("Delivered message:")
        print(message)
        if pre_timestamp > 0:
            next_time = timestamp - pre_timestamp
            next_time = next_time / speed_up_factor
            time.sleep(next_time)
        pre_timestamp = timestamp
    producer.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='BitTorrent message producer')
    parser.add_argument('--file', type=str, default=FILENAME, help='Input JSON file path')
    parser.add_argument('--broker', type=str, default='localhost:9092', help='Kafka broker address')
    parser.add_argument('--speed', type=float, default=1.0, help='Speed up factor')
    args = parser.parse_args()

    producer = KafkaProducer(bootstrap_servers=[args.broker])

    replay_messages(args.file, producer, args.speed)