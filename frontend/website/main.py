from flask import Flask, render_template
from collectAndAnalyzeRequestor import sendRequest
from pymongo import MongoClient
from dowCompanyFetcher import dowFetcher

app = Flask(__name__)

stockDict = dowFetcher()
sendRequest(stockDict, "collectorQ", "collectorKey")

cluster = MongoClient("mongodb://localhost:27017/")
database = cluster["analyzed_data_db"]
collection = database["analyzed_data"]

@app.route("/")
def main_page():

    cursor = collection.find({})
    display_list = []
    for document in cursor:
        display_list.append(document)

    print(type("main_page.html"))

    return render_template("main_page.html", display_list = display_list)

if __name__ == '__main__': 
    app.run(debug=True)