from flask import Flask, render_template
from collectAndAnalyzeRequestor import sendRequest
from pymongo import MongoClient
from dowCompanyFetcher import dowFetcher
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

cluster = MongoClient(os.getenv('MONGO_URI'))
database = cluster["analyzed_data_db"]
collection = database["analyzed_data"]

stockDict = dowFetcher()

@app.route("/")
def main_page():

    sendRequest(stockDict, "collectorQ", "collectorKey")

    cursor = collection.find({})
    display_list = []
    for document in cursor:
        display_list.append(document)

    return render_template("main_page.html", display_list = display_list)

if __name__ == "__main__":
    app.run(debug=True)
    #from waitress import serve
    #serve(app, host="0.0.0.0", port=5000)