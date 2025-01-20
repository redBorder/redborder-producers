#!/usr/bin/python3
from faker import Faker
import time
import random
from assets import random_malicious_ip, user_devices, random_vendor
import argparse
from sensors import get_random_sensor
from producer import run_producer

# Inicializa Faker para datos sintéticos
fake = Faker()

address = [
  "192.0.2.1",
  "203.0.113.5",
  "185.220.100.4",
  "45.76.123.45",
  "104.16.90.1",
  "172.16.0.10",
  "10.0.0.25",
  "192.168.1.1",
  "198.51.100.23",
  "203.0.113.42"
]
address_malicious = ["80.66.76.130", "91.238.181.32", "185.170.144.3", "185.234.216.88"]

# Definición de las firmas para el sig_id y sus revisiones (rev)
sig_ids = [
  (2018853, 1, 'ET WEB_CLIENT Possible Phishing E-ZPass Email Toll Notification July 30 2014', 'low'),
  # (2022136, 1, 'ET WEB_CLIENT Netsolhost SSL Proxying - Possible Phishing Nov 24 2015', 'low'),
  # (2022974, 1, 'ET CURRENT_EVENTS Suspicious SMTP Settings in XLS - Possible Phishing Document', 'low'),
  # (2023139, 1, 'ET INFO Form Data Submitted to yolasite.com - Possible Phishing', 'low'),
  (2022374, 1, 'ET WEB_CLIENT Suspicious LastPass URI Structure - Possible Phishing', 'high'),
  (2022486, 1, 'ET CURRENT_EVENTS Possible Phishing Landing via GetGoPhish Phishing Tool', 'high'),
  (2022578, 1, 'ET WEB_CLIENT JS Obfuscation - Possible Phishing 2016-03-01', 'medium'),
  (2022597, 1, 'ET CURRENT_EVENTS Possible Phishing Landing - Data URI Inline Javascript Mar 07 2016', 'high'),
  (2022905, 1, 'ET CURRENT_EVENTS Suspicious Hidden Javascript Redirect - Possible Phishing Jun 17', 'high'),
  (2023638, 1, 'ET WEB_CLIENT Possible Phishing Redirect Dec 13 2016', 'high')
]

# Función para generar eventos sintéticos relacionados con redes
def generate_event():
  sig_id_data = random.choice(sig_ids)
  user_asset = random.choice(user_devices)
  dst_port = random.choice([80, 443, 53, 25, 587, 465, 143, 993, 110, 995])
  src = random.choice(random_malicious_ip)
  dst = user_asset[0]
  return {
    "timestamp": int(time.time()),
    "sensor_id_snort": 0,
    "action": "alert",
    "sig_generator": 1,
    "sig_id": sig_id_data[0],  # ID del evento
    "rev": sig_id_data[1],  # Revisión asociada al evento
    "priority": sig_id_data[3],
    "msg": sig_id_data[2],  # Descripción del mensaje
    "classification": "Phising",
    "l4_proto_name": "udp",
    "l4_proto": 17,
    "ethsrc": fake.mac_address(),
    "ethdst": user_asset[1],
    "ethsrc_vendor": random_vendor(),
    "ethdst_vendor": user_asset[3],
    "ethtype": 33024,
    "vlan": 30,
    "vlan_name": "30",
    "vlan_priority": 0,
    "vlan_drop": 0,
    "udplength": 72,
    "ethlength": 0,
    "ethlength_range": "0(0-64]",
    "src_port": 3478,
    "src_port_name": "3478",
    "dst_port": dst_port,
    "dst_port_name": str(dst_port),
    "src_asnum": 4110056778,
    "src": src,
    "src_name": src,
    "dst_asnum": 3038642698,
    "dst_name": dst,
    "dst": dst,
    "ttl": 47,
    "tos": 0,
    "id": 0,
    "iplen": 92,
    "iplen_range": "[64-128)",
    "dgmlen": 92,
    "sensor_type": "ips",
    "domain_name": "N/A",
    "index_partitions": 5,
    "index_replicas": 1,
    **get_random_sensor('ips') # Merge sensor data
  }

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('-d', '--duration', type=int, default=5, help='Duration in seconds (default: 5)')
  args = parser.parse_args()
  run_producer(generate_event, args.duration, topic='rb_event', time_range=(1, 1))
