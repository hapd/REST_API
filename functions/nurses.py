# System Imports
import datetime
import json

def process_add_new_nurse(req, client):
    res = {}
    print("Request:",req)
    currentId = client.data.nurses.count_documents({})
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