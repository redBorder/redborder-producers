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
  (48871, 1, 'MALWARE-OTHER Win.Trojan.Mimikatz inbound payload download', 'High'),
  (61287, 1, 'INDICATOR-COMPROMISE Win.Tool.WinPWN toolkit PrintNightmare download attempt', 'Medium'),
  (61288, 1, 'INDICATOR-COMPROMISE Win.Tool.WinPWN toolkit PrintNightmare download attempt', 'Medium'),
  (50463, 1, 'INDICATOR-COMPROMISE Mimikatz use via SMB attempt', 'High'),
  (50467, 1, 'INDICATOR-COMPROMISE Mimikatz use via SMB attempt', 'High'),
  (52442, 1, 'MALWARE-OTHER Win.Trojan.Mimikatz variant download attempt', 'High'),
  (52443, 1, 'MALWARE-OTHER Win.Trojan.Mimikatz variant download attempt', 'High'),
  (59982, 1, 'MALWARE-OTHER Win.Trojan.Mimikatz binary download', 'High'),
  (59983, 1, 'MALWARE-OTHER Win.Trojan.Mimikatz binary download', 'High'),
  (61225, 1, 'INDICATOR-COMPROMISE Win.Tool.WinPWN toolkit Mimikatz download attempt', 'Medium'),
  (61226, 1, 'INDICATOR-COMPROMISE Win.Tool.WinPWN toolkit Mimikatz download attempt', 'Medium'),
  (61227, 1, 'INDICATOR-COMPROMISE Win.Tool.WinPWN toolkit Mimikatz download attempt', 'Medium'),
  (61287, 1, 'INDICATOR-COMPROMISE Win.Tool.WinPWN toolkit PrintNightmare download attempt', 'Medium'),
  (61288, 1, 'INDICATOR-COMPROMISE Win.Tool.WinPWN toolkit PrintNightmare download attempt', 'Medium'),
]

# Función para generar eventos sintéticos relacionados con redes
def generate_event():
  sig_id_data = random.choice(sig_ids)
  src = "74.125.250.244"
  lan_device = random.choice(user_devices_2)
  return {
    "timestamp": int(time.time()),
    "sensor_id_snort": 0,
    "action": "alert",
    "sig_generator": 1,
    "classification": "Misc activity",
    "sig_id": sig_id_data[0],  # ID del evento
    "rev": sig_id_data[1],  # Revisión asociada al evento
    "priority": sig_id_data[3],
    "msg": sig_id_data[2],  # Descripción del mensaje
    "l4_proto_name": "udp",
    "l4_proto": 17,
    "ethsrc": "ec:ce:13:ae:32:a3",
    "ethdst": lan_device.mac,
    "ethsrc_vendor": "Cisco Systems, Inc",
    "ethdst_vendor": lan_device.vendor,
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
    "src_name": str(src),
    "dst_asnum": "3038642698",
    "dst_name": lan_device.name,
    "dst": lan_device.ip,
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
