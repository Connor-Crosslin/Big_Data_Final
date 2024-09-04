from frontend.website.collectAndAnalyzeRequestor import sendRequest
from frontend.website.dowCompanyFetcher import dowFetcher
import unittest
import json

class TestDowFetcher(unittest.TestCase):
    def test_dow_fetcher(self):
        #make sure fetcher returns dictionary of size 30
        fetcherResult = dowFetcher()
        #print(fetcherResult)
        self.assertEqual(len(fetcherResult), 30)
        self.assertEqual(type(fetcherResult), type({}))

class testCollectAndAnalyzeRequestor(unittest.TestCase):
    def testCollector(self):
        stockDict = {"0": "AAPL"}
        messageSent = sendRequest(stockDict, "collectorQ", "collectorKey")
        self.assertEqual(messageSent, True)

    def testRequestor(self):
        messageSent = sendRequest(json.dumps({"ticker" : "AAPL"}), "analyzerQ", "analyzerKey")
        self.assertEqual(messageSent,True)

if __name__ == "__main__":
    unittest.main()