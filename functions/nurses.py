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
    image = req["image"]
    del req["image"]
    newNurse = req
    newNurse['_id'] = int(currentId+1)
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
        image = client.images.nurses.find_one({'_id': int(nurse_id)})
        res["fullfilmentText"] = "True"
        res["data"] = {"data": return_without_password(nurse), "image": image}
    except:
        res["fullfilmentText"] = "False"
    res["source"] = "hapd-api"
    res = json.dumps(res, indent = 4)
    return res

def process_update_nurse(nurse_id, req, client):
    res = {}
    data = req
    query = {'_id': nurse_id}
    try:
        if('image' in req):
            updatedResult = client.images.nurses.update_one(query, {"$set": data['image']})
            if(updatedResult.raw_result["updatedExisting"] == True):
                res["fullfilmentText"] = "True"
                del data["image"]
            else:
                res["fullfilmentText"] = "False"
                res["source"] = "webhook-hapd-api"
                res = json.dumps(res, indent=4)
                return res
        elif('nop' in req):
            if(req['operation'] == 'increment'):
                updatedResult = client.data.nurses.update_one(query, {'$inc': {"nop": 1}})
            else:
                updatedResult = client.data.nurses.update_one(query, {'$set': {"nop": data["nop"]}})
            if(updatedResult.raw_result["updatedExisting"] == True):
                res["fullfilmentText"] = "True"
            else:
                res["fullfilmentText"] = "False"
        elif('nos' in req):
            if(req['operation'] == 'increment'):
                updatedResult = client.data.nurses.update_one(query, {'$inc': {"nos"+req['stage']: 1}})
            else:
                updatedResult = client.data.nurses.update_one(query, {'$set': {"nos"+req['stage']: req['nos']}})
            if(updatedResult.raw_result["updatedExisting"] == True):
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
