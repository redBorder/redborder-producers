#!/usr/bin/python3
import argparse
from faker import Faker
import json
import time
import random
import string
from datetime import datetime
from producers import run_producer
from assets import lan_devices_2

# Inicializa Faker para datos sintéticos
fake = Faker()

# Funciones para generar datos
def get_random_message():
  msg_names = [
    'ET SCAN Nmap TCP Connect Scan Detected',
    'ET SCAN Potential SYN Scan Detected',
    'ET SCAN TCP NULL Scan Detected',
    'ET SCAN TCP FIN Scan Detected',
    'ET SCAN TCP Xmas Scan Detected',
    'ET SCAN Potential UDP Scan Detected',
    'ET SCAN Port Sweep Detected',
    'ET SCAN ICMP Sweep Detected',
    'ET SCAN Unusual Port Scanning Detected',
    'ET SCAN Behavioral Unusual Port 80 Traffic Detected',
    'ET SCAN Possible HTTP GET Flood Detected',
    'ET SCAN Potential SSH Scan Detected',
    'ET SCAN Potential SMB Scan Detected',
    'ET SCAN Behavioral Anomalous Port Scanning Detected',
    'ET SCAN High Number of Connection Attempts Detected',
    'ET SCAN Potential FTP Bounce Scan Detected',
    'ET SCAN Unusual Network Reconnaissance Detected',
    'ET SCAN Possible DNS Zone Transfer Attempt',
    'ET SCAN Suspicious Port Scanning Activity Detected',
    'ET SCAN Unusual Outbound Port Scan Detected',
    'ET SCAN Behavior Consistent with Port Scanning Detected',
  ]
  return random.choice(msg_names)

def get_random_app():
  app_names = [
    "brave-browser.desktop",
    "chrome.desktop",
    "firefox.desktop",
    "mysql.service",
    "apache2.service",
    "nginx.service",
    "ssh.service",
    "vsftpd.service",
    "systemd.service",
    "docker.service"
  ]
  return random.choice(app_names)

# Cargar datos de archivos JSON
def load_json_data(file_path):
  with open(file_path, 'r') as file:
    return json.load(file)

def generate_hostname():
  prefix = random.choice(['host', 'server', 'node', 'machine', 'localhost'])
  suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
  return f"{prefix}-{suffix}"

# Función para generar errores SSL o de red de ejemplo
def generate_error_message():
  errors = [
    "handshake failed; returned -1, SSL error code 1, net_error -202",
    "connection reset; SSL error code 5, net_error -105",
    "certificate validation failed; SSL error code 3, net_error -201",
    "socket timeout; returned -1, SSL error code 2, net_error -204"
  ]
  return random.choice(errors)

# Función para generar raw_message y message
def generate_raw_message(hostname, app_name, procid):
  timestamp = datetime.now().strftime("%b %d %H:%M:%S")  # Ej: "Oct 23 15:22:15"
  error_message = generate_error_message()

  # raw_message incluye todos los elementos
  raw_message = f"<14>{timestamp} {hostname} {app_name}[{procid}]: [266809:266815:1023/{datetime.now().strftime('%H%M%S')}.078218:ERROR:ssl_client_socket_impl.cc(882)] {error_message}"

  # message es el contenido del mensaje de error
  message = f"[266809:266815:1023/{datetime.now().strftime('%H%M%S')}.078218:ERROR:ssl_client_socket_impl.cc(882)] {error_message}"

  return raw_message, message

# Función para generar eventos de vault
def generate_vault():
  data = load_json_data('vault.json')
  vault_data = random.choice(data['vaults'])  # Selecciona un vault aleatorio
  hostname = generate_hostname()
  app_name = get_random_app()
  procid = random.randint(1000, 9999)

  raw_message, message = generate_raw_message(hostname, app_name, procid)
  lan_device = random.choice(lan_devices_2)
  vault_data.update({
    "timestamp": int(time.time()),
    "hostname": hostname,
    "fromhost_ip": lan_device.ip,
    "app_name": app_name,
    "raw_message": raw_message,
    "syslogseverity_text": random.choice(['notice', 'info', 'critical', 'emergency']),
    "message": message
  })
  return vault_data

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('-d', '--duration', type=int, default=-1, help='Duration in seconds (default: 5)')
  args = parser.parse_args()
  run_producer(generate_vault, args.duration, topic='rb_event', time_range=(5, 60))
