#!/usr/bin/python3
import argparse
from faker import Faker
import time
import random
# from assets import lan_devices, random_wan, wan_devices
import assets
from vulnerability import Vulnerability
from producer import run_producer
from sensors import get_random_sensor

fake = Faker() # Useful to generate random values depending on the field

# Función para generar eventos sintéticos relacionados con redes

EVENT_FOR_NEXT_EVENT=10
def generate_event():
  lan_device = random.choice(assets.lan_devices_2)
  timestamp = int(time.time())
  vulnerabilitys = Vulnerability.make_vulnerabilities()
  vulnerability = vulnerabilitys[EVENT_FOR_NEXT_EVENT*int(time.time()) % vulnerabilitys.__len__()]
  return {
    "timestamp": timestamp,
    "ipv4": lan_device.ip,
    "os": lan_device.os,
    **vulnerability.get_data(),
    **get_random_sensor('scanner')
  }

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('-d', '--duration', type=int, default=5, help='Duration in seconds (default: 5), -1 for infinite')
  args = parser.parse_args()
  run_producer(
    callback=generate_event,
    duration=args.duration,
    topic='rb_flow',
    time_range=(EVENT_FOR_NEXT_EVENT, EVENT_FOR_NEXT_EVENT)
  )

