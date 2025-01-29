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
  (34284, 1, 'SERVER-WEBAPP ESF pfSense firewall_rules cross site scripting attempt', 'high')
]

# Función para generar eventos sintéticos relacionados con redes
def generate_event():
  sig_id_data = random.choice(sig_ids)
  src = "74.125.250.244"
  user_device = random.choice(user_devices_2)
  return {
    "timestamp": int(time.time()),
    "sensor_id_snort": 0,
    "action": "alert",
    "sig_generator": 1,
    "sig_id": sig_id_data[0],  # ID del evento
    "rev": sig_id_data[1],  # Revisión asociada al evento
    "msg": sig_id_data[2],  # Descripción del mensaje
    "priority": sig_id_data[3],
    "classification": "Misc activity",
    "l4_proto_name": "udp",
    "l4_proto": 17,
    "ethsrc": "ec:ce:13:ae:32:a3",
    "ethdst": user_device.mac,
    "ethsrc_vendor": "Cisco Systems, Inc",
    "ethdst_vendor": user_device.vendor,
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
    "dst_port": 55759,
    "dst_port_name": "55759",
    "src_asnum": 4110056778,
    "src": src,
    "src_name": src,
    "dst_asnum": "3038642698",
    "dst_name": user_device.name,
    "dst": user_device.ip,
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
