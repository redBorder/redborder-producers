#!/usr/bin/python3
from kafka import KafkaProducer
from faker import Faker
import json
import time
import random
import ipaddress
from datetime import datetime, timedelta

# Configura el productor de Kafka
producer = KafkaProducer(
  bootstrap_servers=['localhost:9092'],
  value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Inicializa Faker para datos sintéticos
fake = Faker()

# Diccionario con rangos de IP por categoría
ip_ranges = {
  "NetDevices": ("192.168.0.1", "192.168.0.254"),
  "Admin": ("192.168.1.1", "192.168.1.254"),
  "IT": ("192.168.2.1", "192.168.2.254"),
  "Users": ("192.168.3.1", "192.168.4.254"),
  "Guests": ("192.168.10.1", "192.168.11.254"),
}

# Cargar datos de archivos JSON
def load_json_data(file_path):
  with open(file_path, 'r') as file:
    return json.load(file)

# Función para generar direcciones IP realistas
def generate_ip():
  return fake.ipv4_public()  # Genera IPs privadas (puedes cambiar a ipv4_public si necesitas IPs públicas)

def generate_mac():
  return fake.mac_address()

def generate_port():
  return random.randint(1024, 65535)

def generate_ip_from_range(ip_range):
  # Convierte el rango a objetos de IP y genera una IP aleatoria dentro de ese rango
  start_ip = int(ipaddress.IPv4Address(ip_range[0]))
  end_ip = int(ipaddress.IPv4Address(ip_range[1]))
  random_ip = random.randint(start_ip, end_ip)
  return str(ipaddress.IPv4Address(random_ip))


# Función para generar eventos de flujo (netflow)
def generate_flow(data):
  flow_data = random.choice(data['flows'])  # Selecciona un flujo aleatorio
  
  # Selecciona un rango de IP al azar del diccionario ip_ranges
  category = random.choice(list(ip_ranges.keys()))
  ip_range = ip_ranges[category]

  # Genera IPs dentro del rango seleccionado
  lan_ip = generate_ip_from_range(ip_range)
  wan_ip = generate_ip_from_range(ip_range)

  flow_data.update({
    "timestamp": int(time.time()),
    "flow_id": random.randint(1000, 9999),
    "type": random.choice(["netflowv10", "netflowv9"]),
    "direction": random.choice(["downstream", "upstream"]),
    "lan_ip": lan_ip,
    "wan_ip": wan_ip,
    "public_ip": generate_ip(),
    "client_mac": generate_mac(),
    "lan_l4_port": generate_port(),
    "wan_l4_port": generate_port(),
    "bytes": random.randint(100000, 800000),
    "pkts": random.randint(500, 5000)
  })
  return flow_data

# Función para intercalar la generación de eventos y enviar a diferentes topics
def send_interleaved_events():
  data = load_json_data('data_traffic.json')  # Cargar el archivo unificado
  event_generators = [
    (generate_flow, 'rb_flow'),
  ]

  try:
    while True:
      event_func, topic = random.choice(event_generators)
      event_data = event_func(data)
      if event_data:
        producer.send(topic, value=event_data)
        print(f'Data sent to {topic}: {event_data}')
      time.sleep(random.uniform(0.5, 2.5))  # Simular picos de tráfico
  except KeyboardInterrupt:
    pass
  finally:
    producer.close()

# Llama a la función para comenzar a enviar los eventos
send_interleaved_events()
