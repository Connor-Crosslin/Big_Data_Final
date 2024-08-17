from collectAndAnalyzeRequestor import sendRequest
from pymongo import MongoClient
from dowCompanyFetcher import dowFetcher

stockDict = dowFetcher()
sendRequest(stockDict, "collectorQ", "collectorKey")
#sendRequest("AAPL", "analyzerQ", "analyzerKey")

