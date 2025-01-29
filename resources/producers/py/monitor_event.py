import random

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