# !/usr/bin/env python
import pika
from flask import Flask

app = Flask(__name__)

def callback(ch, method, properties, body):
    print(" [x] Mensaje recibido:", body)

@app.route('/send')
def send():
    print('Conectando a RabbitMQ')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
    channel = connection.channel()
    channel.queue_declare(queue='micro-seguridad')
    channel.basic_publish(exchange='',
                          routing_key='micro-seguridad',
                          body='Hello micro seguridad!')

    print(" [x] Sent 'Hello World!'")

    connection.close()

    return 'Hola micro rabbit!'

@app.route('/read')
def read():
    print('Conectando a RabbitMQ')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
    channel = connection.channel()
    channel.queue_declare(queue='micro-seguridad')

    def callback(ch, method, properties, body):
        return(f" [x] readed: {body}")

    channel.basic_consume(queue='micro-seguridad', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


    print(" [x] read 'Hello World!'")


    return 'Hola micro rabbit!'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
