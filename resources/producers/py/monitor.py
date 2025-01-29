#!/usr/bin/python3
import argparse
import time
from sensors import get_random_sensor
from producer import run_producer
from monitor_event import MonitorEvent

def generate_event():
  #TODO: All monitors, not just one by one
  monitors = MonitorEvent.generate_all_monitors()
  monitor = monitors[int(time.time()) % monitors.__len__()]
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
  parser.add_argument('-l', '--looptime', type=int, default=1, help='Loop time in seconds (default: 300)') # 1 sec until fix monitor multi event
  args = parser.parse_args()
  run_producer(callback=generate_event, duration=args.duration, topic='rb_monitor', time_range=(args.looptime, args.looptime))