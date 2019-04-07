# System Imports
import datetime
import json

def return_without_password(a):
    del a["password"]
    return a

def process_add_new_patient(req, client):
    res = {}
    print("Request: ", req)
    year = str(req.get('dob')).split("/")[2]
    age = datetime.datetime.now().year - int(year)
    currentId = client.data.patients.count_documents({})
    newPatient = {
        "_id": int(currentId+1),
        "name": req.get('name'),
        "password": req.get('password'),
        "nurse": req.get('nurse'),
        "age": int(age),
        "dob": req.get('dob'),
        "stage": req.get('stage'),
        "gender": req.get('gender'),
        "contact": req.get('contact'),
        "bloodgroup": req.get('bloodgroup'),
        "nurse_id": int(req.get('nurse_id')),
        "address": req.get('address')
    }
    try:
        dbId = client.data.patients.insert_one(newPatient).inserted_id
        res["fullfilmentText"] = "True"
        res["PID"] = str(dbId)
    except:
        res["fullfilmentText"] = "False"
    try:
        updatedResult = client.data.nurses.update_one({"_id": int(req.get("nurse_id"))}, {"$inc": {"nop": 1, "nos"+req.get("stage"): 1}})
        if(updatedResult.raw_result["updatedExisting"] == True):
            res["fullfilmentText"] = "True"
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
        res["fullfilmentText"] = "True"
        res["data"] = return_without_password(patient)
    except:
        res["fullfilmentText"] = "False"
    res["source"] = "webhook-hapd-api"
    res = json.dumps(res, indent = 4)
    print("Response:", res)
    return res

def process_get_patient_groupby_nurse_id(nurse_id, req, client):
    res = {}
    try:
        patients_iter = client.data.patients.find({"nurse_id": nurse_id})
        patients = [return_without_password(patient) for patient in patients_iter]
        res["fullfilmentText"] = "True"
        res["data"] = patients
    except:
        res["fullfilmentText"] = "False"
    res["source"] = "webhook-hapd-api"
    res = json.dumps(res, indent = 4)
    return res

def process_update_patient(patient_id, req, client):
    print("Request:", req)
    res = {}
    try:
        query = {'_id': patient_id}
        fields = ['name', 'dob', 'address', 'stage', 'bloodgroup', 'gender', 'password']
        unverifiedFields = req.keys()
        data = {}
        preStage = ""
        nurse_id = ""
        for field in unverifiedFields:
            if(field in fields):
                if(field == "stage"):
                    patient = client.data.patients.find_one({'_id': int(patient_id)})
                    preStage = patient.get("stage")
                    nurse_id = patient.get("nurse_id")
                data[field] = req[field]
        updatedResult = client.data.patients.update_one(query, {'$set': data})
        if(updatedResult.raw_result["updatedExisting"] == True):
            res["fullfilmentText"] = "True"
            if("stage" in unverifiedFields):
                updatedResult2 = client.nurses.update_one({'_id': int(nurse_id)}, {"$inc": {"nos"+str(preStage): -1}})
                if(updatedResult2.raw_result["updatedExisting"] == True):
                    updatedResult3 = client.nurses.update_one({'_id': int(nurse_id)}, {"$inc": {"nos"+str(req["stage"]): 1}})
        else:
            res["fullfilmentText"] = "False"
    except:
        print("Error in updating the document in the Database.")
        res["fullfilmentText"] = "False"
    res["source"] = "webhook-hapd-api"
    res = json.dumps(res, indent=4)
    return res

def process_delete_patient(patient_id, client):
    res = {}
    try:
        query = {'_id': patient_id}
        deletedResult = client.data.patients.delete_one(query)
        if(deletedResult.deleted_count == 1):
            res["fullfilmentText"] = "True"
        else:
            res["fullfilmentText"] = "False"
    except:
        res["fullfilmentText"] = "False"
    res["source"] = "hapd-api"
    res = json.dumps(res, indent=4)
    return res

def process_authenticate_patient(req, client):
    res = {}
    print('Request:', req)
    try:
        patient_id = req.get('patient_id')
        password = req.get('password')
        if(password == client.data.patients.find_one({'_id': patient_id})["password"]):
            res["fullfilmentText"] = "Access granted"
        else:
            res["fullfilmentText"] = "Access denied"
    except:
        res["fullfilmentText"] = "False"
    res["source"] = "webhook-hapd-api"
    res = json.dumps(res, indent = 4)
    print("Response:", res)
    return res
