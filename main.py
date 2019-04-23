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
from functions.patients import process_add_new_patient
from functions.patients import process_get_patient
from functions.patients import process_authenticate_patient
from functions.patients import process_update_patient
from functions.patients import process_get_patient_groupby_nurse_id
from functions.patients import process_delete_patient
from functions.nurses import process_add_new_nurse
from functions.nurses import process_get_nurse
from functions.nurses import process_update_nurse
from functions.nurses import process_authenticate_nurse
from functions.schedules import process_add_schedule
from functions.schedules import process_get_schedule
from functions.schedules import process_update_schedule
from functions.schedules import process_delete_schedule

client = pymongo.MongoClient("mongodb+srv://hapd:majorproject19@cluster0-vm7gp.mongodb.net/test?retryWrites=true")

app = Flask(__name__)

# Routes for Patients
@app.route('/patients', methods=['POST'])
def add_new_patient():
    res = process_add_new_patient(request.get_json(silent=True, force=True), client)
    r = make_response(res)
    r.headers["Content-Type"] = "application/json"
    return r

@app.route('/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    print(patient_id)
    res = process_get_patient(patient_id, request.get_json(silent=True, force=True), client)
    r = make_response(res)
    r.headers["Content-Type"] = "application/json"
    return r

@app.route('/patients/nurse/<int:nurse_id>', methods=['GET'])
def get_patient_groupby_nurse_id(nurse_id):
    res = process_get_patient_groupby_nurse_id(nurse_id, request.get_json(silent=True, force=True), client)
    r = make_response(res)
    r.headers["Content-Type"] = "application/json"
    return r

@app.route('/patients/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    res = process_update_patient(patient_id, request.get_json(silent=True, force=True), client)
    r = make_response(res)
    r.headers["Content-Type"] = "application/json"
    return r

@app.route('/patients/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    res = process_delete_patient(patient_id, client)
    r = make_response(res)
    r.headers["Content-Type"] = "application/json"
    return r


@app.route('/patients/authenticate', methods=['POST'])
def authenticate_patient():
    res = process_authenticate_patient(request.get_json(silent=True, force=True), client)
    r = make_response(res)
    r.headers["Content-Type"] = "application/json"
    return r


# Routes for Nurses
@app.route('/nurses', methods=['POST'])
def add_new_nurse():
    res = process_add_new_nurse(request.get_json(silent=True, force=True), client)
    r = make_response(res)
    r.headers["Content-Type"] = "application/json"
    return r

@app.route('/nurses/<int:nurse_id>', methods=['GET'])
def get_nurse(nurse_id):
    print(nurse_id)
    res = process_get_nurse(nurse_id, request.get_json(silent=True, force=True), client)
    r = make_response(res)
    r.headers["Content-Type"] = "application/json"
    return r

@app.route('/nurses/<int:nurse_id>', methods=['PUT'])
def update_nurse(nurse_id):
    res = process_update_nurse(nurse_id, request.get_json(silent=True, force=True), client)
    r = make_response(res)
    r.headers["Content-Type"] = "application/json"
    return r

@app.route('/nurses/authenticate', methods=['POST'])
def authenticate_nurse():
    res = process_authenticate_nurse(request.get_json(silent=True, force=True), client)
    r = make_response(res)
    r.headers["Content-Type"] = "application/json"
    return r

# Route for Schedules
@app.route('/schedules', methods=['POST'])
def add_schedule():
    res = process_add_schedule(request.get_json(silent=True, force=True), client)
    r = make_response(res)
    r.headers["Content-Type"] = "application/json"
    return r

@app.route('/schedules/<int:patient_id>', methods=['GET'])
def get_schedule(patient_id):
    res = process_get_schedule(patient_id, client)
    r = make_response(res)
    r.headers["Content-Type"] = "application/json"
    return r

@app.route('/schedules/<int:patient_id>', methods=['PUT'])
def update_schedule(patient_id):
    res = process_update_schedule(patient_id, request.get_json(silent=True, force=True), client)
    r = make_response(res)
    r.headers["Content-Type"] = "application/json"
    return r

@app.route('/schedules/<int:patient_id>', methods=['DELETE'])
def delete_schedule(patient_id):
    res = process_delete_schedule(patient_id, client)
    r = make_response(res)
    r.headers["Content-Type"] = "application/json"
    return r

if(__name__ == "__main__"):
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')

