#!/usr/bin/python3
import argparse
from faker import Faker
import time
import random
from assets import user_devices_2
from sensors import get_random_sensor
from producer import run_producer

# Inicializa Faker para datos sintéticos
fake = Faker()

# Definición de las firmas para el sig_id y sus revisiones (rev)
sig_ids = [
  (2029329, 1, 'ET WEB_CLIENT Possible Embedded NTLM Hash Theft Code', 'high'),
  (31289, 1, 'SERVER-WEBAPP /etc/passwd file access attempt', 'high')
]

# Función para generar eventos sintéticos relacionados con redes
def generate_event():
  sig_id_data = random.choice(sig_ids)
  user_device = user_devices_2[2] #PC Carlos
  return {
    "timestamp": int(time.time()),
    "sensor_id_snort": 0,
    "action": "alert",
    "sig_generator": 1,
    "sig_id": sig_id_data[0],  # ID del evento
    "rev": sig_id_data[1],  # Revisión asociada al evento
    "msg": sig_id_data[2],  # Descripción del mensaje
    "priority": sig_id_data[3],
    "src_name": user_device.name,
    "src": user_device.ip,
    "ethsrc": user_device.mac,
    "ethsrc_vendor": user_device.vendor,
    "classification": "Misc activity",
    "l4_proto_name": "udp",
    "l4_proto": 17,
    "ethdst": "50:eb:f6:8e:cf:30",
    "ethdst_vendor": "ASUSTek COMPUTER INC.",
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
    "dst_asnum": 3038642698,
    "dst_name": "88.198.16.134",
    "dst": "88.198.16.134",
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
