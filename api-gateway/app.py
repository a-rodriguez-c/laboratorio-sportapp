from flask import Flask
import requests
from monitor import health_check

app = Flask(__name__)

# MONITOREO DE MICRO-SERVICIOS
# micros = ['localhost:8081', 'localhost:8082', 'localhost:8083', 'localhost:8084'] // local test
micros = ['micro-seguridad:5000', 'micro-naturales:5000', 'micro-notificaciones:5000', 'micro-usuarios:5000']
health_check(micros)


@app.route('/ping')
def health_check():
    return "ok"


@app.route('/seguridad')
def micro_seguridad():
    try:
        return requests.get('http://micro-seguridad:5000/').text
    except requests.exceptions.RequestException as e:
        return "micro-seguridad:5000 is down"


@app.route('/naturales')
def micro_naturales():
    try:
        return requests.get('http://micro-naturales:5000/').text
    except requests.exceptions.RequestException as e:
        return "micro-naturales:5000 is down"


@app.route('/notificaciones')
def micro_notificaciones():
    try:
        return requests.get('http://micro-notificaciones:5000/').text
    except requests.exceptions.RequestException as e:
        return "micro-notificaciones:5000 is down"


@app.route('/usuarios')
def micro_usuarios():
    try:
        return requests.get('http://micro-usuarios:5000/').text
    except requests.exceptions.RequestException as e:
        return "micro-usuarios:5000 is down"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
