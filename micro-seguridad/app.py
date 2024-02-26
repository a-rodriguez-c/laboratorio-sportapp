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

connection = con_rabbitmq()
channel = connection.channel()
channel.exchange_declare(exchange='events', exchange_type='topic')


@app.route('/eventos-seguridad', methods=['POST'])
def eventos_seguridad():
    data = request.get_json()

    event_data = {
        'event_type': data['event_type'],
        'location': data['location'],
        'severity': data['severity'],
    }

    cache.rpush('eventos_seguridad', json.dumps(event_data))
    channel.basic_publish(exchange='events', routing_key='seguridad', body=json.dumps(event_data))

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

channel.queue_declare(queue='eventos_seguridad_queue')
channel.queue_bind(exchange='events', queue='eventos_seguridad_queue', routing_key='seguridad')
channel.basic_consume(queue='eventos_seguridad_queue', on_message_callback=callback, auto_ack=True)

@app.route('/', methods=['GET'])
def index():
    return 'Servicio de eventos seguridad'



@app.route('/ping', methods=['GET'])
def monitor_ping():
    return 'Ok'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')