import pika
import json

def sendRequest(body, queueName, routing_key):

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='main_exchange', exchange_type='direct')

    channel.queue_declare(queue=queueName)

    channel.basic_publish(exchange='main_exchange', routing_key=routing_key, body=json.dumps(body))

    print(f" [x] Sent stock dictionary")

    messageSentSuccess = True

    connection.close()