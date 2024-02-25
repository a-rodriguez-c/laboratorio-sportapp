from flask_socketio import socketio, emit
import redis
from flask import Flask, render_template


app = Flask(__name__)

cache = redis.Redis(host='redis', port=6379)

#Pagina inicial
@app.route('/notificaciones', methods=['POST'])
def notificaciones():
    return render_template('notificaciones.html')

#Manejador de evento para enviar notificaciones
@socketio.on ('send_notofication')
def handle_notification(notification):
    emit('receive_notification', notification, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True)
    