#!/usr/bin/python3
from faker import Faker
import time
import random
from assets import lan_devices, random_malicious_ip, random_port
from producer import run_producer
from sensors import get_random_sensor

# Inicializa Faker para datos sintéticos
fake = Faker()

# Definición de las firmas para el sig_id y sus revisiones (rev)
sig_ids = [
  (49987, 3, 'SERVER-WEBAPP Cisco Prime Infrastructure arbitrary file upload to tftpRoot attempt', 'low'),
  (52129, 3, 'SERVER-WEBAPP Cisco Prime Infrastructure directory traversal attempt', 'low'),
  (57581, 3, 'SERVER-WEBAPP Cisco Prime Infrastructure EPNM command injection attempt', 'medium'),
  (57582, 3, 'SERVER-WEBAPP Cisco Prime Infrastructure EPNM command injection attempt', 'medium'),
  (57583, 3, 'SERVER-WEBAPP Cisco Prime Infrastructure EPNM command injection attempt', 'medium'),
  (58169, 1, 'SERVER-WEBAPP Microsoft Windows Open Management Infrastructure remote code execution attempt', 'high'),
  (59750, 3, 'SERVER-WEBAPP Cisco Enterprise NFV Infrastructure command injection attempt', 'medium'),
  (59751, 3, 'SERVER-WEBAPP Cisco Enterprise NFV Infrastructure command injection attempt', 'medium'),
  (2033690, 1, 'ET TROJAN Cobalt Strike Infrastructure CnC Domain in DNS Lookup', 'high'),
  (2033691, 1, 'ET TROJAN Cobalt Strike Infrastructure CnC Domain in DNS Lookup', 'high')
]

# Función para generar eventos sintéticos relacionados con redes
def generate_event():
  sig_id_data = random.choice(sig_ids)
  lan_asset = lan_devices[5] # web server
  http_port = random.choice([80, 443])
  return {
    "timestamp": int(time.time()),
    "src_port": random_port(),
    "src_port_name": str(random_port()),
    "dst_port": http_port,
    "dst_port_name": str(http_port),
    "src_asnum": 4110056778,
    "src": random_malicious_ip(),
    "src_name": random_malicious_ip(),
    "dst_asnum": "3038642698",
    "dst_name": lan_asset[0],
    "dst": lan_asset[0],
    "ethsrc": fake.mac_address(),
    "ethdst": lan_asset[1],
    "ethsrc_vendor": random,
    "ethdst_vendor": lan_asset[2],
    "sensor_id_snort": 0,
    "action": "alert",
    "sig_generator": 1,
    "sig_id": sig_id_data[0],  # ID del evento
    "rev": sig_id_data[1],  # Revisión asociada al evento
    "priority": sig_id_data[3],
    "classification": "Command and Control",
    "msg": sig_id_data[2],  # Descripción del mensaje
    "l4_proto_name": "udp",
    "l4_proto": 17,
    "ethtype": 33024,
    "vlan": 30,
    "vlan_name": "30",
    "vlan_priority": 0,
    "vlan_drop": 0,
    "udplength": 72,
    "ethlength": 0,
    "ethlength_range": "0(0-64]",
    "ttl": 47,
    "tos": 0,
    "id": 0,
    "iplen": 92,
    "iplen_range": "[64-128)",
    "dgmlen": 92,
    "domain_name": "N/A",
    "index_partitions": 5,
    "index_replicas": 1,
    **get_random_sensor('ips') # Merge sensor data
  }

if __name__ == "__main__":
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument('-d', '--duration', type=int, default=5, help='Duration in seconds (default: 5)')
  args = parser.parse_args()
  run_producer(generate_event, args.duration, topic='rb_event', time_range=(1, 1))
