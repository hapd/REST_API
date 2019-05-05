# System Imports
import datetime
import json

def return_without_password(a):
    del a["password"]
    return a

def process_add_new_nurse(req, client):
    res = {}
    print("Request:",req)
    currentId = client.data.nurses.count_documents({})
    newNurse = req
    newNurse["_id"] = int(currentId+1)
    newNurse["nop"] = 0
    newNurse["nos1"] = 0
    newNurse["nos2"] = 0
    newNurse["nos3"] = 0
    newNurse["nos4"] = 0
    newNurse["nos5"] = 0
    try:
        dbId = client.data.nurses.insert_one(newNurse).inserted_id
        res["nurse_id"] = int(dbId)
        res["fullfilmentText"] = "True"
    except:
        res["fullfilmentText"] = "False"
    res["source"] = "hapd-api"
    res = json.dumps(res, indent = 4)
    return res

def process_get_nurse(nurse_id, req, client):
    res = {}
    try:
        nurse = client.data.nurses.find_one({'_id': int(nurse_id)})
        res["fullfilmentText"] = "True"
        res["data"] = return_without_password(nurse)
    except:
        res["fullfilmentText"] = "False"
    res["source"] = "hapd-api"
    res = json.dumps(res, indent = 4)
    return res

def process_return_password(req, client):
    res = {}
    nurse_id = req.get("nurse_id")
    nurse_id = int(nurse_id)
    try:
        nurse = client.data.nurses.find_one({'_id': nurse_id})
        res["fullfilmentText"] = "True"
        res["data"] = {"password": nurse["password"]}
    except:
        res["fullfilmentText"] = "True"
    res["source"] = "hapd-api"
    res = json.dumps(res, indent = 4)
    return res

def process_update_nurse(nurse_id, req, client):
    res = {}
    query = {'_id': nurse_id}
    try:
        if('nop' in req):
            if(req['operation'] == 'increment'):
                updatedResult = client.data.nurses.update_one(query, {'$inc': {"nop": 1}})
            else:
                updatedResult = client.data.nurses.update_one(query, {'$set': {"nop": req["nop"]}})
            if(updatedResult.raw_result["updatedExisting"] == True):
                del req["nop"]
                res["fullfilmentText"] = "True"
            else:
                res["fullfilmentText"] = "False"
        elif('nos' in req):
            if(req['operation'] == 'increment'):
                updatedResult = client.data.nurses.update_one(query, {'$inc': {"nos"+req['stage']: 1}})
            else:
                updatedResult = client.data.nurses.update_one(query, {'$set': {"nos"+req['stage']: req['nos']}})
            if(updatedResult.raw_result["updatedExisting"] == True):
                del req["stage"]
                del req["nos"]
                res["fullfilmentText"] = "True"
            else:
                res["fullfilmentText"] = "False"
        else:
            updatedResult = client.data.nurses.update_one(query, {'$set': req})
            if(updatedResult.raw_result["updatedExisting"] == True):
                res["fullfilmentText"] = "True"
            else:
                res["fullfilmentText"] = "False"
    except:
        print("Error in updating the document in the Database.")
        res["fullfilmentText"] = "False"
    res["source"] = "hapd-api"
    return json.dumps(res, indent=4)

def process_authenticate_nurse(req, client):
    res = {}
    nurse_id = req.get("nurse_id")
    password = req.get("password")
    if(client.data.nurses.find_one({"_id": int(nurse_id)})["password"] == password):
        res["fullfilmentText"] = "True"
    else:
        res["fullfilmentText"] = "False"
    res["source"] = "hapd-api"
    return json.dumps(res, indent=4)
