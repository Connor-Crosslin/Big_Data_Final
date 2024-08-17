import requests
from pymongo import MongoClient
import json
import pika

def callback(ch, method, properties, body):

    print("collectorWorker is working")

    cluster = MongoClient("mongodb://localhost:27017/")
    database = cluster["raw_data_db"]
    collection = database["raw_data"]

    stockDict = json.loads(body)
    
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    #loop through the stockDict and see if the stock data exists already
    #if it does, send a message to the exchange for the analzyerQ saying data is ready
    # if it doesnt, add the data to teh raw data dict first THEN send the message to the analyzer Q
    
    for company in stockDict.values():
        print(company)
        existing_data = collection.find_one({'symbol':company})
        print(existing_data)
        if existing_data == None: #data doesnt exist yet
            response = requests.get('https://financialmodelingprep.com/api/v3/balance-sheet-statement/' + str(company) + '?period=annual&apikey=RTwVW0uEPtekbFchrNyJkqtUcym6fWfT')
            response_dict = response.json()[0]
            collection.insert_one(response_dict)
                
        channel.basic_publish(exchange='main_exchange', routing_key="analyzerKey", body=str(company))
        


    print("collectorWorker executed")


