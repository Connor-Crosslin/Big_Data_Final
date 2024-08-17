from pymongo import MongoClient

def callback(ch, method, properties, body):

    print("analyzerWorker is working")
    print(body)
    
    cluster = MongoClient("mongodb://localhost:27017/")
    raw_database = cluster["raw_data_db"]
    raw_collection = raw_database["raw_data"]

    analyzed_database = cluster["analyzed_data_db"]
    analyzed_collection = analyzed_database["analyzed_data"]
    analyzed_collection.drop()

    raw_data = raw_collection.find({})

    for balance_sheet in raw_data:

        tempTotalAssets = balance_sheet['totalAssets']
        tempTotalLiabilities = balance_sheet['totalLiabilities']
        tempSE = balance_sheet['totalStockholdersEquity']
        dict_to_insert = {'_id' : balance_sheet['symbol'], 'date':balance_sheet['date'], 'debtToAssets':(tempTotalLiabilities/tempTotalAssets), 'debtToEquity':(tempTotalLiabilities/tempSE)}
        analyzed_collection.insert_one(dict_to_insert)
    
    cursor = analyzed_collection.find({})

    for document in cursor:
        print("in the second forloop", document) 

    print("analyzerWorker executed")
