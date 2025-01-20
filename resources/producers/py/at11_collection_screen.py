#!/usr/bin/python3
import argparse
import time
import random
from datetime import datetime
from faker import Faker
from assets import user_devices_2
from sensors import get_random_sensor
from producer import run_producer

# Inicializa Faker para datos sintéticos
fake = Faker()

# Definición de las firmas para el sig_id y sus revisiones (rev)
sig_ids = [
  (7605, 1, 'MALWARE-BACKDOOR katux 2.0 runtime detection - screen capture', 'info')
]

# Función para generar eventos sintéticos relacionados con redes
def generate_event():
  sig_id_data = random.choice(sig_ids)
  user_device = random.choice(user_devices_2)
  timestamp=time.time()
  date = datetime.fromtimestamp(timestamp).date()
  hostname = user_device.name
  raw = str(date) + ' ' + hostname + ' Microsoft-Windows-Security-Auditing 4624 - An image was captured and saved: C:\\Users\\username\\Pictures\\Powned.png'
  return {
    "app_name": 'Snipping Tool',
    "timestamp": int(timestamp),
    "hostname": user_device.name,
    "fromhost_ip": user_device.ip,
    "raw_message": raw,
    "severity_text": sig_id_data[3],
    "message": sig_id_data[2],
    **get_random_sensor('vault')
  }

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('-d', '--duration', type=int, default=5, help='Duration in seconds (default: 5)')
  args = parser.parse_args()
  run_producer(generate_event, args.duration, topic='rb_vault', time_range=(1, 1))
