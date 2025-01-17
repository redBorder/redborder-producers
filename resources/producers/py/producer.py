from kafka import KafkaProducer
import json
import time
import random
# from traffic import generate_event

# # Define sig_ids list
# sig_ids = [1, 2, 3, 4, 5]  # Add appropriate signature IDs

# Configura el productor de Kafka
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                        value_serializer=lambda v: json.dumps(v).encode('utf-8'))


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