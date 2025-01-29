#!/usr/bin/python3
import time
import random
from assets import random_lan, random_malicious_ip, random_port, random_mac
from sensors import get_random_sensor
from producer import run_producer

# Active Scanning T1595
def generate_active_scanning_event():
    port_src = random_port()
    wan_ip = random_malicious_ip()
    asset_dst = random_lan()

    return {
        "sig_id": 2001583,
        "msg": "ET SCAN Behavioral Unusual Port 1433 traffic Potential Scan or Infection",
        "priority": "low",
        "timestamp": int(time.time()),
        "sensor_id_snort": 0,
        "action": "alert",
        "sig_generator": 1,
        "rev": 3,
        "classification": "Misc activity",
        "l4_proto_name": "udp",
        "l4_proto": 17,
        "ethsrc": random_mac(),
        "ethdst": asset_dst[1],
        "ethsrc_vendor": random.choice(["Cisco Systems, Inc", "Dell Inc.", "HP Inc.", "Intel Corporation", "Apple Inc.", "Samsung Electronics", "Juniper Networks", "IBM Corp.", "Sony Corporation", "LG Electronics", "Huawei Technologies", "ASUS", "Lenovo", "D-Link Corporation", "NetGear", "TP-Link Technologies"]),
        "ethdst_vendor": asset_dst[2], # maybe change between cisco and asus
        "ethtype": 33024,
        "vlan": 30,
        "vlan_name": "30",
        "vlan_priority": 0,
        "vlan_drop": 0,
        "udplength": 72,
        "ethlength": 0,
        "ethlength_range": "0(0-64]",
        "src_port": port_src,
        "src_port_name": str(port_src),
        "dst_port": 1433,
        "dst_port_name": "1433",
        "src_asnum": 4110056778,
        "src": wan_ip,
        "src_name": wan_ip,
        "dst_asnum": "3038642698",
        "dst_name": asset_dst[0],
        "dst": asset_dst[0],
        "ttl": 47,
        "tos": 0,
        "id": 0,
        "iplen": 92,
        "iplen_range": "[64-128)",
        "dgmlen": 92,
        "group_uuid": "f1b4eeb4-12e1-464c-821f-2439564ec585",
        "group_name": "outside",
        "domain_name": "N/A",
        "index_partitions": 5,
        "index_replicas": 1,
        "campus": "N/A",
        "campus_uuid": "N/A",
        "building": "Main building",
        "building_uuid": "8e004910-c5e7-4ca0-b9df-156b1f6ad0a6",
        **get_random_sensor('ips') # Merge sensor data
        }

# Produce mensajes continuamente simulando eventos de escaneo activo

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--duration', type=int, default=5, help='Duration in seconds (default: 5)')
    args = parser.parse_args()
    run_producer(generate_active_scanning_event, args.duration, topic='rb_event', time_range=(1, 1))
