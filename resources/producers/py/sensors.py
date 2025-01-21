#This is a config file where we define on each type of sensors we can produce
from random import choice

"""
Define here your sensors and their attributes. 
To create a new sensor to can do it from the manager web.
To get the data of a sensor use the knife commands:
knife node list
knife node show <sensor_id> -l
"""

#TODO: read this from knife node list and knife node show <sensor> -l

FLOW_SENSORS=[
  {
  # put your sensor here
  } 
  # ,{}
]

#TODO generate the ips sensors from the ips sensors in the 
# To generate a synthetic IPS:
# 1. create a flow sensor with name 'IPS'
# 2. open rails console
# 3. run s=Sensor.all.find_by_name('IPS') && s.type=33 && s.save
IPS_SENSORS=[
  {
    "sensor_type": "ips",
    "sensor_ip": "192.168.0.2",
    "sensor_uuid": "d385c4d9-745e-4e9e-bff2-6273a07fd0de",
    "sensor_name": "IPS",
    # "namespace": "Namespace Level Alfa",
    # "namespace_uuid": "352369f8-60fb-4b72-a603-d1d8393cca0a",
    # "organization": "TechSecure",
    # "organization_uuid": "4b839195-3d3a-4983-abc0-9731ea731cab",
    # "service_provider": "TechSecure Corp",
    # "service_provider_uuid": "c2238202-ce42-4235-814f-91d2e6e0122a",
    # "building": "Main building",
    # "building_uuid": "8e004910-c5e7-4ca0-b9df-156b1f6ad0a6"
  } 
]
# Example of a sensor defined in a demo
# {
  # "sensor_ip": "192.168.0.10",
  # "sensor_name": "Base Router",
  # "sensor_uuid": "08eac42f-bf2d-4996-865f-9f6a4f493f71",
  # "namespace": "Namespace Level Alfa",
  # "namespace_uuid": "352369f8-60fb-4b72-a603-d1d8393cca0a",
  # "organization": "TechSecure",
  # "organization_uuid": "4b839195-3d3a-4983-abc0-9731ea731cab",
  # "service_provider": "TechSecure Corp",
  # "service_provider_uuid": "c2238202-ce42-4235-814f-91d2e6e0122a",
  # "building": "Main building",
  # "building_uuid": "8e004910-c5e7-4ca0-b9df-156b1f6ad0a6"
# }

# These properties can to not be really necessary here: 
#   mac="00:2b:3c:4d:5e:6f",
#   vendor="Cisco Systems, Inc",
#   os="Cisco Unified Communications Manager VoIP adapter",

VAULT_SENSORS=[
  {
    "sensor_type": "vault",
    "sensor_ip": "10.0.50.40",
    "sensor_uuid": "d08a7b60-3b24-4bee-8a6b-fffb91e50791",
    "sensor_name": "wcl-vault",
  }
]

MONITOR_SENSORS=[
  {
    "sensor_type": "monitor",
    "sensor_name": "jenkins-ng",
    "sensor_ip": "10.1.209.254",
    "sensor_uuid": "2f841ca5-69b1-4c0e-874c-b0313328c7e4",
  }
]

def get_random_sensor(type):
  valid_types = ['flow', 'ips', 'vault']
  sensors = []
  if type == 'flow':
    sensors = FLOW_SENSORS
  elif type == 'ips':
    sensors = IPS_SENSORS
  elif type == 'vault':
    sensors = VAULT_SENSORS
  else:
    raise ValueError(f"Not recognized sensor type: {type}. Valid types are: {valid_types}")
  return choice(sensors)
