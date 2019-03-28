# System Imports
import datetime
import json

def process_add_new_patient(req, client):
    res = {}
    year = str(req.get('dob')).split("/")[2]
    age = datetime.datetime.now().year - int(year)
    currentId = client.data.patients.count_documents({})
    newPatient = {
        "_id": (currentId+1),
        "name": req.get('name'),
        "password": req.get('password'),
        "nurse": req.get('nurse'),
        "age": age,
        "dob": req.get('dob'),
        "stage": req.get('stage'),
        "gender": req.get('gender'),
        "contact": req.get('contact'),
        "bloodgroup": req.get('bloodgroup'),
        "nurse_id": req.get('nurseId'),
        "address": req.get('address')
    }
    image_data = {
        "_id": (currentId+1),
        "image": req.get('image')
    }
    try:
        dbId = client.data.patients.insert_one(newPatient).inserted_id
        imageId = client.images.patients.insert_one(image_data).inserted_id
        res["fullfilmentText"] = "True"
        res["PID"] = str(dbId)
        res["ImageID"] = str(imageId)
    except:
        res["fullfilmentText"] = "False"
    res["source"] = "webhook-hapd-api"
    res = json.dumps(res, indent = 4)
    print("Response:", res)
    return res

def process_get_patient(patient_id, req, client):
    res = {}
    try:
        patient = client.data.patients.find_one({'_id': int(patient_id)})
        print(patient["name"])
        res["fullfilmentText"] = "True"
        res["data"] = {
            "pid": str(patient_id),
            "name": patient.get("name"),
            "age": patient.get("age"),
            "dob": patient.get("dob"),
            "stage": patient.get("stage"),
            "gender": patient.get("gender"),
            "bloodgroup": patient.get("bloodgroup"),
            "nurse": patient.get("nurse"),
            "nurse_id": patient.get("nurse_id"),
            "contact": patient.get("contact"),
            "address": patient.get("address")
        }
    except:
        res["fullfilmentText"] = "False"
    res["source"] = "webhook-hapd-api"
    res = json.dumps(res, indent = 4)
    print("Response:", res)
    return res

def process_authenticate_patient(req, client):
    res = {}
    try:
        patient_id = req.get('patient_id')
        password = req.get('password')
        if(password == client.data.patients.find_one({'_id': patient_id})["password"]):
            res["fullfilmentText"] = "True"
        else:
            res["fullfilmentText"] = "False"
    except:
        res["fullfilmentText"] = "False"
    res["source"] = "webhook-hapd-api"
    res = json.dumps(res, indent = 4)
    print("Response:", res)
    return res