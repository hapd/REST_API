# Flask Imports
import flask
from flask import Flask
from flask import request
from flask import make_response

# System Imports
import json
import datetime
import os

# MongoDB Imports
import pymongo

# Local Imports
import functions

client = pymongo.MongoClient("mongodb+srv://hapd:majorproject19@cluster0-vm7gp.mongodb.net/test?retryWrites=true")

app = Flask(__name__)

@app.route('/patients', methods=['POST'])
def add_new_patient():
    res = functions.patients.process_add_new_patient(request.get_json(silent=True, force=True), client)
    r = make_response(res)
    r.headers["Content-Type"] = "application/json"
    return r

@app.route('/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    res = functions.patients.process_get_patient(patient_id, request.get_json(silent=True, force=True), client)
    r = make_response(res)
    r.headers["Content-Type"] = "application/json"
    return r

    


if(__name__ == "__main__"):
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
