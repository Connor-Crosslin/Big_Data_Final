import pika
import collectorWorker
import analyzerWorker
import os
from dotenv import load_dotenv

load_dotenv()

#these are for running on cloudAMPQ
#url = os.getenv('CLOUDAMPQ_URI', 'amqp://guest:guest@localhost:5672/%2f')
#params = pika.URLParameters(url)

params = pika.ConnectionParameters(host=os.getenv('CLOUDAMPQ_URI')) #comment this out if using cloudAMPQ
connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.exchange_declare(exchange='main_exchange', exchange_type='direct')

channel.queue_declare(queue="collectorQ")
channel.queue_declare(queue="analyzerQ")

channel.queue_bind(exchange='main_exchange', queue="collectorQ", routing_key="collectorKey")
channel.queue_bind(exchange='main_exchange', queue="analyzerQ", routing_key="analyzerKey")

channel.basic_consume(queue="collectorQ", on_message_callback=collectorWorker.callback, auto_ack=True)
channel.basic_consume(queue="analyzerQ", on_message_callback=analyzerWorker.callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')

channel.start_consuming()


