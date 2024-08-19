import requests
from pymongo import MongoClient
import json
import pika
import os
from dotenv import load_dotenv

load_dotenv()

def callback(ch, method, properties, body):

    print("collectorWorker is working")

    cluster = MongoClient(os.getenv('MONGO_URI'))
    database = cluster["raw_data_db"]
    collection = database["raw_data"]

    stockDict = json.loads(body)
    
    url = os.getenv('CLOUDAMPQ_URI', 'amqp://guest:guest@localhost:5672/%2f')
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    #loop through the stockDict and see if the stock data exists already
    #if it does, send a message to the exchange for the analzyerQ saying data is ready
    # if it doesnt, add the data to teh raw data dict first THEN send the message to the analyzer Q
    
    for company in stockDict.values():
        existing_data = collection.find_one({'symbol':company})
        #if there were no API call limit, the following line of code would be active:
        #response = requests.get('https://financialmodelingprep.com/api/v3/balance-sheet-statement/' + str(company) + '?period=annual&apikey=RTwVW0uEPtekbFchrNyJkqtUcym6fWfT')

        if existing_data == None: #data doesnt exist yet
            #if there were no API call limit, the following API call would be done outside the if block
            response = requests.get('https://financialmodelingprep.com/api/v3/balance-sheet-statement/' + str(company) + '?period=annual&apikey=RTwVW0uEPtekbFchrNyJkqtUcym6fWfT')
            response_dict = response.json()[0]
            collection.insert_one(response_dict)
        
        #this code would check if each entry was up to date, but is not active due to API call limit since this would execute on each page refresh       
        #elif existing_data[0]['date'] < response.json()[0]['date']: 
            #print(str(company) + " data is out of date! Updating...")
            #collection.delete_many({"_id": str(company)})
            #response_dict = response.json()[0]
            #collection.insert_one(response_dict)

        channel.basic_publish(exchange='main_exchange', routing_key="analyzerKey", body=json.dumps({"ticker" : company}))
        
    print("collectorWorker executed")


