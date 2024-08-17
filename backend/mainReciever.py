import pika
import collectorWorker
import analyzerWorker

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='main_exchange', exchange_type='direct')

channel.queue_bind(exchange='main_exchange', queue="collectorQ", routing_key="collectorKey")
channel.queue_bind(exchange='main_exchange', queue="analyzerQ", routing_key="analyzerKey")

#def collectorCallback(ch, method, properties, body):
#    print(f" [x] COLLECTORCALLBACK {body}")

#def analyzerCallback(ch, method, properties, body):
#    print(f" [x] ANALYZER CALLBACKE {body}")

channel.basic_consume(queue="collectorQ", on_message_callback=collectorWorker.callback, auto_ack=True)
channel.basic_consume(queue="analyzerQ", on_message_callback=analyzerWorker.callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')

channel.start_consuming()

