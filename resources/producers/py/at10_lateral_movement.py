#!/usr/bin/python3
import argparse
from faker import Faker
import time
from assets import user_devices_2, random_port
from sensors import get_random_sensor
from producer import run_producer

fake = Faker()

# Función para generar eventos de escaneo activo (Active Scanning T1595)
def generate_event():
  src_port = random_port()
  dst_port = random_port()
  dst = user_devices_2[0] # Base Router
  src = user_devices_2[2] # PCCarlos
  return {
    "src": src.ip,
    "dst": dst.ip,
    "ethsrc": src.mac,
    "ethdst": dst.mac,
    "src_name": src.name,
    "dst_name": dst.name,
    "ethsrc_vendor": src.vendor,
    "ethdst_vendor": dst.vendor,
    "payload": "73726567417265736f75746f722e436f726574726f737465722e437573746f6d65722e4e65775f4974656d205c4d696170706c69636174696f6e2e70776f772e4b6f706572696e672e417267757365727261636f69737469732e484b43552e5c4d696170706c69636174696f6e5c4d694170706c69636174696f6e205665727375732e486f6c614d756e646f726272696172732e486b43552e4e65775f4974656d205354505265673274636f726574726f737465722e4e65775f4974656d20566973696f6e202053656e64696e672e4d726f6f7420546f6b656e68616d616e204874617420436c61757365",
    "timestamp": int(time.time()),
    "sensor_id_snort": 0,
    "action": "alert",
    "sig_generator": 1,
    "rev": 3,
    "priority": "high",
    "classification": "Trojan",
    "msg": 'POLICY-OTHER use of psexec remote administration tool',
    "sig_id": 24008,  # Selecciona un sig_id aleatorio
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
    "src_port": src_port,
    "src_port_name": str(src_port),
    "dst_port": dst_port,
    "dst_port_name": str(dst_port),
    "src_asnum": 4110056778,
    "dst_asnum": "3038642698",
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
