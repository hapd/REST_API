# System Imports
import datetime
import json

def process_add_schedule(req,client):
    res={}
    print("Request: ",req)
    patient_id=int(req.get('patient_id'))
    task=req.get('task')
    time=req.get('time')
    result = client.data.schedules.find_one({'_id':patient_id})
    if result==None:
        entry={
            '_id': patient_id,
            'tasks': {
                time:task
            }    
        }
        try:
            result_insert=client.data.schedules.insert_one(entry).inserted_id
            res["fullfilmentText"] = "True"
        except:
            res["fullfilmentText"] = "Could not create schedule" 
    else:
        tasks=result.get('tasks')
        if (time not in tasks):
            tasks[time] = task
            try:
                updatedResult = client.data.schedules.update_one({'_id': patient_id}, {'$set': {"tasks": tasks}})
            except:
                res["fullfilmentText"] = "Could not connect to the server"
            if(updatedResult.raw_result["updatedExisting"] == True):
                res["fullfilmentText"] = "True"
            else:
                res["fullfilmentText"] = "Could not update entry"    
        else:
            res["fullfilmentText"] = "Task already exists"
    res["source"] = "hapd-api"
    res = json.dumps(res, indent = 4)
    return res

def process_get_schedule(patient_id, client):
    res = {}
    query = {
        '_id': int(patient_id)
    }
    try:
        result = client.data.schedules.find_one(query)
        if (result == None):
            res["fullfilmentText"] = "No schedule with the given patient id"
        else:
            res["data"] = result
            res["fullfilmentText"] = "True"
    except:
        res["fullfilmentText"] = "Could not connect to the server"
    res["source"] = "hapd-api"
    res = json.dumps(res, indent=4)
    return res

def process_update_schedule(patient_id, req, client):
    res = {}
    query = {'_id': int(patient_id)}
    time = req.get("time")
    tasks = req.get("task")
    old_time = req.get("old_time")
    old_task = req.get("old_task")
    try:
        result = client.data.schedules.find_one(query)
        if (result == None):
            res["fullfilmentText"] = "Schedule does not exists"
        else:
            tasks = result["tasks"]
            if(old_time != time):
                del tasks[old_time]
                tasks[time] = task
            elif(old_task != task):
                k = list(tasks.keys())
                for i in k:
                    if(tasks[i] == old_task):
                        del tasks[i]
                        tasks[time] = task
            updatedResult = client.data.schedules.update_one(query, {"$set":{"tasks": tasks}})
            if(updatedResult.raw_result["updatedExisting"] == True):
                res["fullfilmentText"] = "True"
            else:
                res["fullfilmentText"] = "Could not be updated"
    except Exception as e:
        print(e)
        res["fullfilmentText"] = "Could not connect the server"
    res["source"] = "hapd-api"
    res = json.dumps(res, indent = 4)
    return res

def process_delete_schedule(patient_id, time, client):
    res = {}
    query = {'_id': int(patient_id)}
    try:
        result = client.data.schedules.find_one(query)
        if (result == None):
            res["fullfilmentText"] = "Schedule does not exists"
        else:
            tasks = result["tasks"]
            del tasks[time]
            updatedResult = client.data.schedules.update_one(query, {"$set":{"tasks": tasks}})
            if(updatedResult.raw_result["updatedExisting"] == True):
                res["fullfilmentText"] = "True"
            else:
                res["fullfilmentText"] = "Could not be updated"
    except:
        res["fullfilmentText"] = "Could not connect to the server"
    res["source"] = "hapd-api"
    res = json.dumps(res, indent=4)
    return res
