import json

def process_add_face(patient_id, name, client):
  res = {}
  result = client.data.faces.find_one({'_id': int(patient_id)})
  if(result == None):
    data = {
      '_id': int(patient_id),
      'faces': {
        str(name): 1
      }
    }
    try:
      inserted_id = client.data.faces.insert_one(data).inserted_id
      res["fullfilmentText"] = "True"
    except Exception as e:
      res["fullfilmentText"] = str(e)
  else:
    faces = result['faces']
    names = list(faces.keys())
    if (name not in names):
      faces[name] = 1
    else:
      faces[name] += 1
    try:
      updatedResult = client.data.faces.update_one({'_id': int(patient_id)}, {'$set': {'faces': faces}})
      if(updatedResult.raw_result["updatedExisting"] == True):
        res["fullfilmentText"] = "True"
      else:
        res["fullfilmentText"] = "Could not be updated"
    except Exception as e:
      res["fullfilmentText"] = str(e)
  res["source"] = "hapd-api"
  res = json.dumps(res, indent=4)
  return res
