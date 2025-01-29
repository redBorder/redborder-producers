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
	(2038604, 1, 'ET ATTACK_RESPONSE net user Command Output via HTTP POST', 'medium')
]

# Función para generar eventos sintéticos relacionados con redes
def generate_event():
  sig_id_data = random.choice(sig_ids)
  src = user_devices_2[1] # BobPC
  address_malicious = ["88.198.16.134", '46.17.97.37']
  return {
    "timestamp": int(time.time()),
    "payload": '433a5c3e206e657420757365720a0a557375617269617320656e20656c2073697374656d61206c6f63616c3a0a0a2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d2d0a41646d696e6973747261646f72202020202020202020204c6f63616c202020202020202020202020202020726f626572746f2e706572657a0a7573756172696f31202020202020202020202020202075737561726f320a456c20636f6d616e646f207365206861206c6f677261646f20636f6e206578697461',
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
    "src": src.ip,
    "src_name": src.name,
    "ethsrc_vendor": src.vendor,
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
    "dst_port": 80,
    "dst_port_name": "80",
    "src_asnum": 4110056778,
    "dst_asnum": "3038642698",
    "dst_name": random.choice(address_malicious),
    "dst": random.choice(address_malicious),
    "ttl": 47,
    "tos": 0,
    "id": 0,
    "iplen": 92,
    "iplen_range": "[64-128)",
    "dgmlen": 92,
    "domain_name": "N/A",
    "sensor_ip": "10.0.250.195",
    "index_partitions": 5,
    "index_replicas": 1,
    **get_random_sensor('ips')
  }
if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('-d', '--duration', type=int, default=5, help='Duration in seconds (default: 5)')
  args = parser.parse_args()
  run_producer(generate_event, args.duration, topic='rb_event', time_range=(1, 1))
