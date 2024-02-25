import redis
from flask import Flask, request, jsonify
import json
import pika
import time

app = Flask(__name__)

# Conexión a Redis
cache = redis.Redis(host='redis', port=6379)

# Función para establecer conexión con RabbitMQ
def conectar_rabbitmq():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            return connection
        except pika.exceptions.AMQPConnectionError:
            print("Error de conexión con RabbitMQ. Reintentando en 5 segundos...")
            time.sleep(5)

# Conexión a RabbitMQ
connection = conectar_rabbitmq()
channel = connection.channel()
channel.exchange_declare(exchange='events', exchange_type='topic')

@app.route('/eventos-naturales', methods=['POST'])
def eventos_naturales():
    data = request.get_json()

    # Procesar el evento
    event_data = {
        'event_type': data['event_type'],
        'location': data['location'],
        'severity': data['severity'],
    }

    # Almacenar el evento en Redis
    cache.rpush('eventos_naturales', json.dumps(event_data))

    # Publicar el evento en RabbitMQ
    channel.basic_publish(exchange='events', routing_key='naturales', body=json.dumps(event_data))

    return jsonify({'message': 'Evento publicado'}), 200

@app.route('/eventos-naturales', methods=['GET'])
def get_eventos_naturales():
    events = []
    for event in cache.lrange('eventos_naturales', 0, -1):
        events.append(json.loads(event.decode('utf-8')))

    return jsonify(events), 200

# Función para procesar eventos recibidos de RabbitMQ
def callback(ch, method, properties, body):
    event_data = json.loads(body)
    # Procesar el evento recibido
    print("Evento recibido:", event_data)

# Configurar RabbitMQ para leer eventos
channel.queue_declare(queue='eventos_naturales_queue')
channel.queue_bind(exchange='events', queue='eventos_naturales_queue', routing_key='naturales')
channel.basic_consume(queue='eventos_naturales_queue', on_message_callback=callback, auto_ack=True)

@app.route('/', methods=['GET'])
def index():
    return 'Servicio de eventos naturales'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')