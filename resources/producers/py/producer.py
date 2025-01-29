from kafka import KafkaProducer
from datetime import datetime, timedelta
import json
import time
import random
import os

# Configura el productor de Kafka
producer = KafkaProducer(
  bootstrap_servers=['localhost:9092'],
  value_serializer=lambda v: json.dumps(v).encode('utf-8'))

"""
Run a Kafka producer that sends data to a specified topic.

Args:
  callback: Function that generates the data to be sent
  duration: Time in seconds to run the producer. If negative, runs indefinitely
  topic: Kafka topic to send data to (default: 'rb_flow')
  time_range: Tuple of (min, max) seconds between events (default: (0.000001, 0.01))
"""  
def run_producer(callback, duration, topic='rb_flow', time_range=(0.000001, 0.01)):
  start_time = time.time()
  try:
    while duration < 0 or time.time() - start_time < duration:
      data = callback()
      producer.send(topic, value=data)  # Envía los eventos al topic de Kafka
      print(f'Data sent: {data}')

      time.sleep(random.uniform(*time_range))  # Random interval between events
    pass
  finally:
    producer.close()

TEST_TIME=10
def check_and_kill_process(script, command):
  os.system(f'pkill -f "{command}"')
  time.sleep(5)
  check_process = os.popen(f'pgrep -f "{command}"').read()
  while check_process:
    os.system('figlet "WARNING: Process still running"')
    print(f"Warning: Process for {script} is still running")
    os.system(f'pkill -f "{command}"')
    time.sleep(5)
    check_process = os.popen(f'pgrep -f "{command}"').read()

"""
Run one by one each script in SCRIPTS_PATH equally time spaced.
"""
def period_producer(SCRIPTS_PATH, looptime=3600, fast=False):
  while True:
    for script in SCRIPTS_PATH:
      print('Starting attack script')
      script_name = os.path.basename(script)
      os.system(f'figlet "{script_name}"')   
      # if not os.path.exists(script):
      #   print(f"ERROR: Script {script} not found")
      #   continue
        
      is_yml = script.endswith('.yml')
      command = f'rb_synthetic_producer -r 1 -p 1 -c {script}' if is_yml else f'python3 {script}'
      os.system(f'{command}{"&" if is_yml else ""}')
      time.sleep(10 if is_yml else 5)
      check_and_kill_process(script, command)
      sleep_time = TEST_TIME if fast else looptime/SCRIPTS_PATH.__len__()+1 # equally separated
      time.sleep(sleep_time)        

    next_run = datetime.now() + timedelta(hours=looptime/3600)
    os.system(f'figlet "Repeating scenario at {next_run.strftime("%H:%M")} UTC"')
    time.sleep(looptime)
