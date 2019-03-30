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
    image_data = {
        "_id": (currentId+1),
        "image": image
    }
    try:
        dbId = client.data.nurses.insert_one(newNurse).inserted_id
        imageId = client.images.nurses.insert_one(image_data).inserted_id
        res["nurse_id"] = int(dbId)
        res["image_id"] = int(imageId)
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