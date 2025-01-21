#!/usr/bin/python3
import argparse
import time
import random
import assets
from sensors import get_random_sensor
from producer import run_producer
from monitor_event import MonitorEvent

def generate_event(monitor):
  sensor = random.choice(assets.mirror_devices)
  return {
    'index_partitions':5,
    'index_replicas':1,
    'monitor': monitor.monitor,
    'value': monitor.value,
    'type': monitor.type,
    'unit': monitor.unit,
    'timestamp': int(time.time()),    
    **get_random_sensor('monitor')
  }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--duration', type=int, default=-1, help='Duration in seconds (default: 5), -1 for infinite')
    parser.add_argument('-l', '--looptime', type=int, default=60, help='Loop time in seconds (default: 300)') # 5 minutes
    args = parser.parse_args()
    for monitor in MonitorEvent.generate_all_monitors():
      run_producer(callback=generate_event(monitor), duration=args.duration, topic='rb_monitor', time_range=(args.looptime, args.looptime)) 
