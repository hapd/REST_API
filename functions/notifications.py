import json

def process_add_notification(nurse_id, req, client):
    res = {}
    notification = req.get("notification")
    result = client.data.notifications.find_one({'_id':int(nurse_id)})
    if(result==None):
        entry = {"_id": int(nurse_id), "notifications": [notification]}
        try:
            inserted_id = client.data.notifications.insert_one(entry)
            res["fullfilmentText"] = "True"
        except Exception as e:
            res["fullfilmentText"] = str(e)
    else:
        notifications = result["notifications"]
        notifications.append(notification)
        try:
            updatedResult = client.data.notifications.update_one({'_id': int(nurse_id)}, {'$set': {"notifications": notifications}})
            if(updatedResult.raw_result["updatedExisting"] == True):
                res["fullfilmentText"] = "True"
            else:
                res["fullfilmentText"] = "Could not update entry"
        except:
            res["fullfilmentText"] = "Could not connect to the server"
    res["source"] = "hapd-api"
    res = json.dumps(res, indent = 4)
    return res

def process_get_notification(nurse_id, client):
    res = {}
    query = {'_id': int(nurse_id)}
    try:
        result = client.data.notifications.find_one(query)
        if (result == None):
            res["fullfilmentText"] = "No notifications with the given nurse id"
        else:
            res["data"] = result
            res["fullfilmentText"] = "True"
    except:
        res["fullfilmentText"] = "Could not connect to the server"
    res["source"] = "hapd-api"
    res = json.dumps(res, indent=4)
    return res

def process_delete_notification(nurse_id, req, client):
    res = {}
    query = {'_id': int(nurse_id)}
    notification = req.get("notification")
    try:
        result = client.data.notifications.find_one(query)
        if(result == None):
            res["fullfilmentText"] = "No notifications with the given nurse id"
        else:
            notifications = result["notifications"]
            notifications.remove(notification)
            updatedResult = client.data.notifications.update_one({'_id': int(nurse_id)}, {'$set': {"notifications": notifications}})
            if(updatedResult.raw_result["updatedExisting"] == True):
                res["fullfilmentText"] = "True"
            else:
                res["fullfilmentText"] = "Could not update entry"
    except Exception as e:
        res["fullfilmentText"] = str(e)
    res["source"] = "hapd-api"
    res = json.dumps(res, indent=4)
    return res
        
            
      
  
  
