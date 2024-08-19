from frontend.website.collectAndAnalyzeRequestor import sendRequest
from pymongo import MongoClient
from frontend.website.dowCompanyFetcher import dowFetcher
from subprocess import Popen
import multiprocessing
import time
import os

def integrationTest():

    stockDict = dowFetcher()
    sendRequest(stockDict, "collectorQ", "collectorKey")

if __name__ == '__main__':

    integrationTest()

    cluster = MongoClient(os.getenv('MONGO_URI'))
    database = cluster["analyzed_data_db"]
    collection = database["analyzed_data"]

    cursor = collection.find({})
    testResult = []
    for document in cursor:
        testResult.append(document)

    #print(testResult)
    
    assert type(testResult) == type([]), f"result should a python list, got {type(testResult)}"
    assert len(testResult) == 30, f"result should be of size 30, got {len(testResult)}"
    for item in testResult:
        assert len(item) == 4, f"each item in the result should be of size 4 got {len(item)}"

    print("All tests passed!")








    

