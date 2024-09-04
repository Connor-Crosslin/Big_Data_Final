from flask import Response, Flask, render_template
from collectAndAnalyzeRequestor import sendRequest
from pymongo import MongoClient
from dowCompanyFetcher import dowFetcher
import os
from dotenv import load_dotenv
import prometheus_client
from prometheus_client.core import CollectorRegistry
from prometheus_client import Summary, Counter, Histogram, Gauge
import time

def create_app():
    app = Flask(__name__)
    load_dotenv()

    _INF = float("inf")

    graphs = {}
    graphs['c'] = Counter('python_request_operations_total', 'The total number of processed requests')
    graphs['h'] = Histogram('python_request_duration_seconds', 'Histogram for the duration in seconds.', buckets=(1, 2, 5, 6, 10, _INF))

    cluster = MongoClient(os.getenv('MONGO_URI'))
    database = cluster["analyzed_data_db"]
    collection = database["analyzed_data"]

    stockDict = dowFetcher()

    @app.route("/")
    def main_page():
        start = time.time()
        graphs['c'].inc()

        sendRequest(stockDict, "collectorQ", "collectorKey")

        cursor = collection.find({})
        display_list = []
        for document in cursor:
            display_list.append(document)

        end = time.time()
        graphs['h'].observe(end - start)

        return render_template("main_page.html", display_list = display_list)

    @app.route("/metrics")
    def requests_count():
        res = []
        for k,v in graphs.items():
            res.append(prometheus_client.generate_latest(v))
        return Response(res, mimetype="text/plain")

    return app

#for develpment:
#if __name__ == "__main__":
#   app.run(debug=True)
