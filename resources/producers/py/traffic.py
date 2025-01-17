#!/usr/bin/python3
from kafka import KafkaProducer
from faker import Faker
import json
import time
import random
from random import shuffle
from assets import lan_devices, random_wan, wan_devices
import assets
from weight import day_weights, hour_weights
import argparse
from producer import run_producer
from sensors import get_random_sensor

# Define sig_ids list
sig_ids = [1, 2, 3, 4, 5]  # Add appropriate signature IDs

# Configura el productor de Kafka

fake = Faker()

# Función para generar eventos sintéticos relacionados con redes
def generate_event():
    lan_device = random.choice(assets.lan_devices_2)
    wan_device = random.choice(wan_devices)
    in_out = [lan_device, wan_device]
    shuffle(in_out)
    src_device = in_out[0]
    dst_device = in_out[1]
    sensor = random.choice(assets.mirror_devices)
    direction = 'upstream' if src_device == lan_device else 'downstream'
    domain = '.'.join(wan_device.url.split('.')[-2:])   #remove TLD
    www = 'www.' + domain
    timestamp = int(time.time())
    date = time.localtime(timestamp)
    weight = day_weights[date.tm_wday] * hour_weights[date.tm_hour]    
    pkt = random.randint(10,1000) *weight
    bytes = pkt*100
    return {
        "http_url": www, #"https://www.example.com/path/to/resource?param=value",
        "referer": www, #"https://www.example.com/path/to/resource?param=value",
        "http_host": www, #"www.example.com",
        "host": www, #"www.example.com",
        "http_host_l2": domain, #"example.com",
        "host_l2_domain": domain, #"example.com",
        "referer_l2": domain, #"example.com",
        "http_user_agent": fake.user_agent(),
        "type": "netflowv10",
        "ip_protocol_version": 4,
        "l4_proto": 17, 
        "l4_proto_name": "udp",
        "input_vrf": 0, 
        "flow_end_reason": "idle timeout",
        # "biflow_direction": "initiator",
        "application_id_name": assets.random_application(), 
        "engine_id_name": "13",
        "output_vrf": 0, 
        "lan_interface": 1, 
        "lan_interface_name": "1", 
        "lan_interface_description": "LAN Interface",
        "wan_interface": 14, "wan_interface_name": "14",
        "wan_interface_description": "WAN Interface",
        "client_mac_vendor": "Cisco Systems",
        "index_partitions": 5, 
        "index_replicas": 1, 
        "direction": direction, 
        "lan_ip": lan_device.ip, 
        "wan_ip": wan_device.ip,
        "public_ip": wan_device.ip, 
        "client_mac": sensor.mac,
        "lan_l4_port": assets.random_port(),
        "wan_l4_port": assets.random_port(),
        "bytes": bytes,
        "pkts": pkt,        
        "timestamp": timestamp,
        **get_random_sensor('flow')
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--duration', type=int, default=-1, help='Time during the producer is working in seconds (default: -1 = infinite)')
    args = parser.parse_args()
    run_producer(callback=generate_event, duration=args.duration, topic='rb_flow', time_range=(0.000001, 0.01))