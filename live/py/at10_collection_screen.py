#!/usr/bin/env python3
from kafka import KafkaProducer
from faker import Faker
import json
import time
import random

# Configura el productor de Kafka
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                        value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Inicializa Faker para datos sintéticos
fake = Faker()

# Campos a modificar
priority_level = ['high', 'medium', 'low']
address = [
    "192.0.2.1",
    "203.0.113.5",
    "185.220.100.4",
    "45.76.123.45",
    "104.16.90.1",
    "172.16.0.10",
    "10.0.0.25",
    "192.168.1.1",
    "198.51.100.23",
    "203.0.113.42"
]
address_malicious = ["80.66.76.130", "91.238.181.32", "185.170.144.3", "185.234.216.88"]

# Definición de las firmas para el sig_id y sus revisiones (rev)
sig_ids = [
    (7605, 1, 'MALWARE-BACKDOOR katux 2.0 runtime detection - screen capture')
]

# Función para generar direcciones IP realistas
def generate_ip():
    return fake.ipv4_private()  # Genera IPs privadas (puedes cambiar a ipv4_public si necesitas IPs públicas)

# Función para generar eventos sintéticos relacionados con redes
def generate_event():
    sig_id_data = random.choice(sig_ids)
    return {
        "timestamp": int(time.time()),
        "sensor_id_snort": 0,
        "action": "alert",
        "sig_generator": 1,
        "sig_id": sig_id_data[0],  # ID del evento
        "rev": sig_id_data[1],  # Revisión asociada al evento
        "priority": random.choice(priority_level),
        "classification": "Misc activity",
        "msg": sig_id_data[2],  # Descripción del mensaje
        "l4_proto_name": "udp",
        "l4_proto": 17,
        "ethsrc": "ec:ce:13:ae:32:a3",
        "ethdst": "50:eb:f6:8e:cf:30",
        "ethsrc_vendor": "Cisco Systems, Inc",
        "ethdst_vendor": "ASUSTek COMPUTER INC.",
        "ethtype": 33024,
        "vlan": 30,
        "vlan_name": "30",
        "vlan_priority": 0,
        "vlan_drop": 0,
        "udplength": 72,
        "ethlength": 0,
        "ethlength_range": "0(0-64]",
        "src_port": 3478,
        "src_port_name": "3478",
        "dst_port": 55759,
        "dst_port_name": "55759",
        "src_asnum": 4110056778,
        "src": random.choice(address),
        "src_name": "74.125.250.244",
        "dst_asnum": "3038642698",
        "dst_name": "10.2.30.181",
        "dst": "10.2.30.181",
        "ttl": 47,
        "tos": 0,
        "id": 0,
        "iplen": 92,
        "iplen_range": "[64-128)",
        "dgmlen": 92,
        "group_uuid": "f1b4eeb4-12e1-464c-821f-2439564ec585",
        "group_name": "outside",
        "sensor_type": "ips",
        "domain_name": "N/A",
        "sensor_ip": "10.0.250.195",
        "index_partitions": 5,
        "index_replicas": 1,
        "sensor_uuid": "df699ecd-fc05-41fd-a0a3-87ecd7da2245",
        "sensor_name": "rbips-62ac2c7d",
        "namespace": "Namespace Level Alfa",
        "namespace_uuid": "352369f8-60fb-4b72-a603-d1d8393cca0a",
        "organization": "TechSecure",
        "organization_uuid": "4b839195-3d3a-4983-abc0-9731ea731cab",
        "service_provider": "TechSecure Corp",
        "service_provider_uuid": "c2238202-ce42-4235-814f-91d2e6e0122a",
        "campus": "N/A",
        "campus_uuid": "N/A",
        "building": "Main building",
        "building_uuid": "8e004910-c5e7-4ca0-b9df-156b1f6ad0a6"
    }

# Produce mensajes continuamente
message_count = 0

def run_producer(duration):
    start_time = time.time()
    try:
        while duration < 0 or time.time() - start_time < duration:
            data = generate_event()
            producer.send('rb_event', value=data)  # Envía los eventos al topic de Kafka
            print(f'Data sent: {data}')
            time.sleep(1)  # Intervalo entre eventos
    except KeyboardInterrupt:
        pass
    finally:
        producer.close()
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--duration', type=int, default=5, help='Duration in seconds (default: 5)')
    args = parser.parse_args()
    run_producer(args.duration)
