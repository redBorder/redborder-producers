import json
import time
import kafka

# Configurar el productor de Kafka
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',  # Cambia esto si tu Kafka está en otro host
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def replay_messages(json_file, topic_name):
    # Cargar los mensajes
    with open(json_file, 'r') as file:
        messages = json.load(file)

    # Tomar el timestamp del primer mensaje como referencia
    start_timestamp = messages[0]['timestamp']
    
    # Registrar el tiempo real de inicio
    real_start_time = time.time()

    for message in messages:
        # Calcular el tiempo relativo al primer mensaje
        elapsed_original = message['timestamp'] - start_timestamp

        # Esperar el tiempo necesario para sincronizar
        while time.time() < real_start_time + elapsed_original:
            time.sleep(0.001)  # Evitar consumir CPU en espera activa

        # Enviar el mensaje a Kafka
        producer.send(topic_name, value=message)
        print(f"Mensaje enviado: {message}")

    print("Reproducción de mensajes completada.")

if __name__ == "__main__":
    # Archivo JSON con los mensajes
    json_file = "mensajes.json"  # Cambia esto al nombre real de tu archivo
    topic_name = "mi-topic"  # Cambia esto al nombre del topic en Kafka

    replay_messages(json_file, topic_name)
