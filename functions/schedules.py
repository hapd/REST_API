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
            res["tasks"] = tasks
            res["fullfilmentText"] = "Task already exists"
    res["source"] = "hapd-api"
    res = json.dumps(res, indent = 4)
    return res
