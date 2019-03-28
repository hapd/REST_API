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
        "pin": req.get('pin'),
        "nurse": req.get('nurse'),
        "age": age,
        "dob": req.get('dob'),
        "stage": req.get('stage'),
        "gender": req.get('gender'),
        "contact": req.get('contact'),
        "bloodgroup": req.get('bloodgroup'),
        "nurse_id": req.get('nurseId')
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
        patient = client.data.patients.find_one({'_id': patient_id})
        res["fullfilmentText"] = "True"
        res["data"] = {
            "patient_id": patient["_id"],
            "name": patient["name"],
            "nurse": patient["nurse"],
            "age": patient["age"],
            "dob": patient["dob"],
            "stage": patient["stage"],
            "gender": patient["gender"],
            "contact": patient["contact"],
            "bloodgroup": patient["bloodgroup"],
            "nurse_id": patient["nurse_id"] 
        }
    except:
        res["fullfilmentText"] = "False"
    res["source"] = "webhook-hapd-api"
    res = json.dumps(res, indent = 4)
    print("Response:", res)
    return res