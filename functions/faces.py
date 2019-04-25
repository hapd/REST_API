import json

def process_add_acquaintance(patient_id, name, relation, client):
  res = {}
  result = client.data.faces.find_one({'_id': int(patient_id)})
  if(result == None):
    data = {
      '_id': int(patient_id),
      'faces': {
        str(name): {
          'relation': str(relation),
          'number-of-images': 0
        }
      }
    }
    try:
      inserted_id = client.data.faces.insert_one(data).inserted_id
      res["fullfilmentText"] = "True"
    except Exception as e:
      res["fullfilmentText"] = str(e)
  else:
    faces = result["faces"]
    names = list(faces.keys())
    if(name not in names):
      faces[name] = {
        'relation': str(relation),
        'number-of-images': 0
      }
      try:
        updatedResult = client.data.faces.update_one({"_id": int(patient_id)}, {"$set": {"faces": faces}})
        if(updatedResult.raw_result["updatedExisting"] == True):
          res["fullfilmentText"] = "True"
        else:
          res["fullfilmentText"] = "Could not be updated"
      except Exception as e:
        res["fullfilmentText"] = str(e)
  res["source"] = "hapd-api"
  res = json.dumps(res, indent=4)
  return res

def process_add_face(patient_id, name, client):
  res = {}
  result = client.data.faces.find_one({'_id': int(patient_id)})
  if(result == None):
    res["fullfilmentText"] = "False"
  else:
    faces = result['faces']
    names = list(faces.keys())
    if (name not in names):
      res["fullfilmentText"] = "False"
    else:
      faces[name]["number-of-images"] += 1
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

def process_get_faces(patient_id, client):
  res = {}
  result = client.data.faces.find_one({'_id': int(patient_id)})
  if(result == None):
    res["fullfilmentText"] = "False"
  else:
    res["fullfilmentText"] = "True"
    res["data"] = result
  res["source"] = "hapd-api"
  res = json.dumps(res, indent=4)
  return res
