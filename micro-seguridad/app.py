import redis
from flask import Flask, request, jsonify
import json
import pika
import time

app = Flask(__name__)


cache = redis.Redis(host='redis', port=6379)


def con_rabbitmq():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            return connection
        except pika.exceptions.AMQPConnectionError:
            print("Error de conexión con RabbitMQ. Reintentando en 5 segundos...")
            time.sleep(5)



@app.route('/eventos-seguridad', methods=['POST'])
def eventos_seguridad():
    data = request.get_json()

    event_data = {
        'event_type': data['event_type'],
        'location': data['location'],
        'severity': data['severity'],
    }

    cache.rpush('eventos_seguridad', json.dumps(event_data))

    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    connection.channel().queue_declare(queue='eventos_seguridad', durable=True)
    connection.channel().basic_publish(
        exchange='',
        routing_key='eventos_seguridad',
        body=json.dumps(event_data),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent

        ))
    connection.close()

    return jsonify({'message': 'Evento publicado'}), 200

@app.route('/eventos-seguridad', methods=['GET'])
def get_eventos_seguridad():
    events = []
    for event in cache.lrange('eventos_seguridad', 0, -1):
        events.append(json.loads(event.decode('utf-8')))

    return jsonify(events), 200


def callback(ch, method, properties, body):
    event_data = json.loads(body)

    print("Evento recibido:", event_data)


@app.route('/', methods=['GET'])
def index():
    return 'Servicio de eventos seguridad'



@app.route('/ping', methods=['GET'])
def monitor_ping():
    return 'Ok'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')