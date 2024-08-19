import pika
import json
import os
from dotenv import load_dotenv

load_dotenv()

def sendRequest(body, queueName, routing_key):

    url = os.getenv('CLOUDAMPQ_URI', 'amqp://guest:guest@localhost:5672/%2f')
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.exchange_declare(exchange='main_exchange', exchange_type='direct')

    channel.queue_declare(queue=queueName)

    channel.basic_publish(exchange='main_exchange', routing_key=routing_key, body=json.dumps(body))

    print(f" [x] Sent stock dictionary")

    messageSentSuccess = True

    connection.close()

    return messageSentSuccess