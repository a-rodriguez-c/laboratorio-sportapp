import redis
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Conexión a Redis: Se establece una conexión con el servidor Redis. En este caso, se asume que Redis está ejecutándose en el mismo contenedor con el nombre de host redis en el puerto predeterminado 6379.
cache = redis.Redis(host='redis', port=6379)

@app.route('/eventos-naturales', methods=['POST'])
def eventos_naturales():
    data = request.get_json()

    # Procesar el evento
    event_data = {
        'event_type': data['event_type'],
        'location': data['location'],
        'severity': data['severity'],
    }

    # Almacenar el evento en Redis para persistencia temporal
    cache.rpush('eventos_naturales', json.dumps(event_data))

    # Enviar el evento a RabbitMQ para procesamiento asíncrono
    # (Aquí necesitarías una configuración adicional para establecer la conexión con RabbitMQ)
    #channel.basic_publish(exchange='events', routing_key='natural_events_queue', body=json.dumps(event_data))

    return jsonify({'message': 'Evento publicado'}), 200

@app.route('/eventos-naturales', methods=['GET'])
def get_eventos_naturales():
    events = []
    for event in cache.lrange('eventos_naturales', 0, -1):
        events.append(json.loads(event.decode('utf-8')))

    # Enviar los eventos a RabbitMQ para procesamiento asíncrono
    # (Aquí necesitarías una configuración adicional para establecer la conexión con RabbitMQ)
    #channel.basic_publish(exchange='events', routing_key='natural_events_queue', body=json.dumps(events))

    return jsonify(events), 200

@app.route('/', methods=['GET'])
def index():
    return 'Servicio de eventos naturales'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')