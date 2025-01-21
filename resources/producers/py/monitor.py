#!/usr/bin/python3
import argparse
import time
import random
import assets
from sensors import get_random_sensor
from producer import run_producer


# Función para generar eventos sintéticos relacionados con redes
NS= "352369f8-60fb-4b72-a603-d1d8393cca0a"
def generate_event(monitor):
  sensor = random.choice(assets.mirror_devices)
  return {
    "index_partitions":5,
    "index_replicas":1,
    'monitor': monitor.monitor,
    'value': monitor.value,
    'type': monitor.type,
    'unit': monitor.unit,
    "timestamp": int(time.time()),
    **get_random_sensor('monitor')
  }

class MonitorEvent:
  MONITOR_CONFIGS = {
    'cpu': {            'unit': '%', 'value_range': (30.0, 50.0), 'type': 'op'},
    'memory': {         'unit': '%', 'value_range': (30.0, 50.0), 'type': 'op'},
    'memory_buffer': {  'unit': '%', 'value_range': (30.0, 50.0), 'type': 'op'},
    'memory_cache': {   'unit': '%', 'value_range': (30.0, 50.0), 'type': 'op'},
    'swap': {           'unit': '%', 'value_range': (30.0, 50.0), 'type': 'system'},
    'disk_load': {      'unit': '%', 'value_range': (30.0, 50.0), 'type': 'system'},
    'pch_temp': {       'unit': 'celsius', 'value_range': (25, 50), 'type': 'system', 'is_int': True},
    'system_temp': {    'unit': 'celsius', 'value_range': (25, 50), 'type': 'system', 'is_int': True},
    'avio': {           'unit': '%', 'value_range': (30.0, 50.0), 'type': 'system'},
    'disk': {           'unit': '%', 'value_range': (1.0, 10.0), 'type': 'snmp'},
    'fan': {            'unit': 'rpm', 'value_range': (1000, 5000), 'type': 'system'}
  }    
  def __init__(self, type: str):
    # if type not in ['cpu', 'memory', 'disk', 'network', 'system_temp', 'avio', 'fan', 'load_1', 'disk_load']:
    #     raise ValueError("Invalid monitor type. Must be one of: cpu, memory, disk, network, system_temp, avio, fan, load_1, disk_load")
    self.monitor = type
    self.define_by_type()
  
  @classmethod
  def generate_all_monitors(cls):
    """
    cls es una referencia a la clase misma (MonitorEvent en este caso).
    Permite acceder a atributos y métodos de la clase sin necesidad de crear una instancia.
    Similar a 'self' pero para métodos de clase en lugar de métodos de instancia.
    """        
    monitor_types = cls.MONITOR_CONFIGS.keys()
    return [MonitorEvent(type) for type in monitor_types]        
  def define_by_type(self):
    try:
      config = self.MONITOR_CONFIGS[self.monitor]
    except KeyError:
      raise ValueError(f"Invalid monitor type. Must be one of: {', '.join(self.MONITOR_CONFIGS.keys())}")
    self.unit = config['unit']
    self.type = config['type']
    if config.get('is_int', False):
      self.value = random.randint(*config['value_range'])
    else:
      self.value = '{:.6f}'.format(random.uniform(*config['value_range']))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--duration', type=int, default=-1, help='Duration in seconds (default: 5), -1 for infinite')
    parser.add_argument('-l', '--looptime', type=int, default=300, help='Loop time in seconds (default: 300)') # 5 minutes
    args = parser.parse_args()
    run_producer(args.duration)
    run_producer(generate_event, args.duration, topic='rb_monitor', time_range=(300, 300)) 
