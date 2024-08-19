from pymongo import MongoClient
import json
import os
from dotenv import load_dotenv

load_dotenv()

def callback(ch, method, properties, body):

    try:
        ticker = json.loads(body)["ticker"] 
    except:
        print("json body in wrong format! Ignoring message")
        return None

    print("analyzerWorker is working on " + ticker)
    
    cluster = MongoClient(os.getenv('MONGO_URI'))
    raw_database = cluster["raw_data_db"]
    raw_collection = raw_database["raw_data"]

    analyzed_database = cluster["analyzed_data_db"]
    analyzed_collection = analyzed_database["analyzed_data"]
    
    raw_data = raw_collection.find({"symbol": ticker})

    analyzed_collection.delete_many({"_id": ticker})

    tempTotalAssets = raw_data[0]['totalAssets']
    tempTotalLiabilities = raw_data[0]['totalLiabilities']
    tempSE = raw_data[0]['totalStockholdersEquity']
    dict_to_insert = {'_id' : raw_data[0]['symbol'], 'date':raw_data[0]['date'], 'debtToAssets':(tempTotalLiabilities/tempTotalAssets), 'debtToEquity':(tempTotalLiabilities/tempSE)}
    
    analyzed_collection.insert_one(dict_to_insert)
    
    #use below code to see data after it is analyzed 
    #cursor = analyzed_collection.find({})
    #for document in cursor:
    #    print("in the second forloop", document) 

    print("analyzerWorker executed")
