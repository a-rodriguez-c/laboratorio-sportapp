import redis
from flask import Flask, request, jsonify


app = Flask(__name__)

memoria = redis.Redis(host='redis', port=6379)

@app.route('/eventos-seguridad', methods=['POST'])
def eventos_seguridad():
    data = request.get_json()

    #procesar el evento
    event_data = {
        'event_type': data['event_type'],
        'location': data['location'],
        'severity': data['severity'],
    }

    # Almacenar el evento en Redis para persistencia temporal
    memoria.rpush('eventos_seguridad', event_data)

    return jsonify({'message': 'Security event received successfully'}), 200

@app.route('/eventos-seguridad', methods=['GET'])
def get_eventos_naturales():
    events = []
    for event in memoria.lrange('eventos_seguridad', 0, -1):
        events.append(event.decode('utf-8'))

    return jsonify(events), 200

    channel.basic_publish(exchange='events', routing_key='natural_events_queue', body=json.dumps(events))

@app.route('/' , methods=['GET'])
def index():
    return 'Servicio de eventos de seguridad'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')