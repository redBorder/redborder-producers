#!/usr/bin/python3
import argparse
from faker import Faker
import time
import random
from assets import lan_devices, random_port
from sensors import get_random_sensor
from producer import run_producer

# Inicializa Faker para datos sintéticos
fake = Faker()

# Definición de las firmas para el sig_id y sus revisiones (rev)
sig_ids = [
  (118, 1, 'MALWARE-BACKDOOR SatansBackdoor.2.0.Beta')
]

# Función para generar eventos sintéticos relacionados con redes
def generate_event():
  sig_id_data = random.choice(sig_ids)
  dst_port = random_port()
  lan = lan_devices[6]#    ("192.168.3.10", "00:8b:9c:0d:1e:2f", "ASUSTek COMPUTER INC."),   #PCAlicia
  lan_ip = lan[0]
  return {
    "timestamp": int(time.time()),
    "sensor_id_snort": 0,
    "action": "alert",
    "sig_generator": 1,
    "sig_id": sig_id_data[0],  # ID del evento
    "rev": sig_id_data[1],  # Revisión asociada al evento
    "priority": 'high',
    "classification": "Malware",
    "msg": sig_id_data[2],  # Descripción del mensaje
    "l4_proto_name": "tdp",
    "l4_proto": 6,
    "ethsrc": fake.mac_address(),
    "ethdst": lan[1],
    "ethsrc_vendor": "Oracle Corporation",
    "ethdst_vendor": lan[2],
    "ethtype": 33024,
    "vlan": 30,
    "vlan_name": "30",
    "vlan_priority": 0,
    "vlan_drop": 0,
    "udplength": 72,
    "ethlength": 0,
    "ethlength_range": "0(0-64]",
    "src_port": dst_port,
    "src_port_name": str(dst_port),
    "dst_port": 443,
    "dst_port_name": "443",
    "src_asnum": 4110056778,
    "src": "31.216.145.5",
    "src_name": "31.216.145.5",
    "dst_asnum": "3038642698",
    "dst_name": lan_ip,
    "dst": lan_ip,
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
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument('-d', '--duration', type=int, default=5, help='Duration in seconds (default: 5)')
  args = parser.parse_args()
  run_producer(generate_event, args.duration, topic='rb_event', time_range=(1, 1))
