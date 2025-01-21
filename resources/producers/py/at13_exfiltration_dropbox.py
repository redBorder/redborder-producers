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
  (2012647, 1, 'ET POLICY Dropbox.com Offsite File Backup in Use', 'medium')
]

# Función para generar eventos sintéticos relacionados con redes
def generate_event():
  sig_id_data = random.choice(sig_ids)
  src = random.choice(user_devices_2)
  return {
    "timestamp": int(time.time()),
    "sensor_id_snort": 0,
    "action": "alert",
    "classification": "Misc activity",
    "sig_generator": 1,
    "sig_id": sig_id_data[0],  # ID del evento
    "rev": sig_id_data[1],  # Revisión asociada al evento
    "priority": sig_id_data[3],
    "msg": sig_id_data[2],  # Descripción del mensaje
    "l4_proto_name": "udp",
    "l4_proto": 17,
    "ethsrc": src.mac,
    "ethdst": "00:1a:2b:3c:4d:5e",
    "ethsrc_vendor": src.vendor,
    "ethdst_vendor": "Cisco Systems, Inc.",
    "ethtype": 33024,
    "vlan": 30,
    "vlan_name": "30",
    "vlan_priority": 0,
    "vlan_drop": 0,
    "udplength": 72,
    "ethlength": 0,
    "ethlength_range": "0(0-64]",
    "src_port": 443,
    "src_port_name": "443",
    "dst_port": 55759,
    "dst_port_name": "55759",
    "src_asnum": 4110056778,
    "src": src.ip,
    "src_name": src.name,
    "dst_asnum": "3038642698",
    "dst_name": "108.160.170.26",
    "dst": "108.160.170.26",
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
