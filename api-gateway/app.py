from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token, JWTManager, decode_token
import requests
from logger import logger

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = "super-secret"

# MONITOREO DE MICRO-SERVICIOS
micros = ['localhost:8081', 'localhost:8082', 'localhost:8083', 'localhost:8084']

blacklist = set()
ips_tries = {}


def blacklisted(ip, reason):
    if ip in blacklist:
        if reason == 'excessive_tries':
            logger.error(f'cliente IP: {ip} - bloqueado por exceso de intentos de acceso no autorizados')
        if reason == 'escalation_privileges':
            logger.error(f'cliente IP: {ip} - bloqueado por intento de escalación de privilegios')
        return True
    return False


def excessive_tries(ip):
    if ip in ips_tries:
        ips_tries[ip] += 1
    if ip not in ips_tries:
        ips_tries[ip] = 1
    if ips_tries[ip] > 5:
        blacklist.add(ip)
        logger.error(f'cliente IP: {ip} - bloqueado por exceso de intentos de acceso no autorizados')
        return True
    return False


def get_user_role(username):
    try:
        resp = requests.get(f'http://127.0.0.1:5000/users/{username}')
        if resp.status_code == 200:
            user_json = resp.json()
            return user_json['role']
        else:
            logger.error(f'Error al obtener el rol del usuario: {resp.status_code} - {resp.text}')
            return None
    except Exception as e:
        logger.warning(f'Error al obtener el rol del usuario: {e}')
        return None


def middleware_authentication():
    logger.info("middleware_authentication")
    token = request.headers.get('Authorization')
    ip_address = request.remote_addr

    if blacklisted(ip_address, 'excessive_tries'):
        return jsonify({"mensaje": "usuario no autorizado"}), 403

    if token is None:
        return jsonify({"mensaje": "usuario no identificado"}), 401
    try:
        token_decoded = decode_token(token[7:])

        if token_decoded['role'] != 'admin' and token_decoded['role'] != 'user':
            blacklist.add(ip_address)
            return jsonify({"mensaje": "usuario no autorizado"}), 403

    except Exception as e:
        if e == 'Signature has expired':
            return jsonify({"mensaje": "token expirado"}), 401

        if excessive_tries(ip_address):
            return jsonify({"mensaje": "usuario no autorizado"}), 403

        logger.warning(f'cliente IP: {ip_address} - error al decodificar token: {e}')
        return jsonify({"mensaje": "usuario no autorizado"}), 403


def middleware_authorization():
    logger.info("middleware_authorization")
    token = request.headers.get('Authorization')
    ip_address = request.remote_addr

    try:
        token_decoded = decode_token(token[7:])
        role = get_user_role(token_decoded['user'])
        if role is None:
            logger.error(f'cliente IP: {ip_address} - error al obtener el rol del usuario')
            return jsonify({"mensaje": "usuario no autorizado"}), 403

        if role != token_decoded['role']:
            if blacklisted(ip_address, 'escalation_privileges'):
                return jsonify({"mensaje": "usuario no autorizado"}), 403

            blacklist.add(ip_address)
            logger.error(f'cliente IP: {ip_address} - bloqueado por intento de escalación de privilegios')
            return jsonify({"mensaje": "usuario no autorizado"}), 403

    except Exception as e:
        if e == 'Signature has expired':
            return jsonify({"mensaje": "token expirado"}), 401

        logger.warning(f'cliente IP: {ip_address} - error al validar autorización de usuario: {e}')
        return jsonify({"mensaje": "usuario no autorizado"}), 403


app.before_request(middleware_authentication)
app.before_request(middleware_authorization)

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
    jwt = JWTManager(app)
    app.run(port=5004)
