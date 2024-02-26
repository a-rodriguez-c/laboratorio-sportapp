import redis
from flask import Flask, request, jsonify
import json
import pika
import time

app = Flask(__name__)

cache = redis.Redis(host='redis', port=6379)


def conn_rabbitmq():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            return connection
        except pika.exceptions.AMQPConnectionError:
            print("Error de conexión con RabbitMQ. Reintentando en 5 segundos...")
            time.sleep(5)

connection = conn_rabbitmq()
channel = connection.channel()
channel.exchange_declare(exchange='events', exchange_type='topic')


@app.route('/notificaciones', methods=['POST'])
def notificaciones():
    data = request.get_json()

    event_data = {
        'event_type': data['event_type'],
        'location': data['location'],
        'severity': data['severity'],
    }

    cache.rpush('notificaciones', json.dumps(event_data))
    channel.basic_publish(exchange='events', routing_key='notificaciones', body=json.dumps(event_data))

    return jsonify({'message': 'Evento notificado'}), 200


@app.route('/notificaciones', methods=['GET'])
def get_notificaciones():
    events = []
    for event in cache.lrange('notificaciones', 0, -1):
        events.append(json.loads(event.decode('utf-8')))

    return jsonify(events), 200


def callback(ch, method, properties, body):
    event_data = json.loads(body)

    print("Evento recibido:", event_data)

channel.queue_declare(queue='eventos_notificaciones_queue')
channel.queue_bind(exchange='events', queue='eventos_notificaciones_queue', routing_key='notificaciones')
channel.basic_consume(queue='eventos_notificaciones_queue', on_message_callback=callback, auto_ack=True)


@app.route('/', methods=['GET'])
def index():
    return 'Servicio de notificaciones'

@app.route('/ping', methods=['GET'])
def monitor_ping():
    return 'Ok'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    