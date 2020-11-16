
import time
import os
import requests
import json
import config as cfg

from pymongo import MongoClient
from pprint import pprint

REQUESTS = {}
time_sleep = 3

def main():

    os.system('cls' if os.name == 'nt' else 'clear')
    print("[SCRIPT] Starting...")

    load_api_to_dict()

    connect_mongodb()
    global DB
    DB = MDB_CLIENT.example

    # create/switch to collection
    bloodCollection = DB.blood
    
    # clear all documents
    bloodCollection.delete_many({})

    populate_collection(bloodCollection)

    while True:
        print("[SCRIPT] sleeping... (+", time_sleep,"s)")
        time.sleep(time_sleep)
        update_collection(bloodCollection)

    print("[SCRIPT] Finished!")

def update_collection(collection):
    
    print("[COLLECTION] updating...")

    load_api_to_dict()

    for req in REQUESTS:
        request = REQUESTS[req]
        medidaNova = {}
        medidaNova["timestamp"] = request["timestamp"]
        medidaNova["bodytemp"] = request["bodytemp"]
        medidaNova["bloodpress_systolic"] = request["bloodpress"]["systolic"]
        medidaNova["bloodpress_diastolic"] = request["bloodpress"]["diastolic"]
        medidaNova["bpm"] = request["bpm"]
        medidaNova["sato2"] = request["sato2"]
        
        arrayMedidas = list(collection.find({"sensorid": request["sensorid"]}, {"_id": 0, "medida": 1})[0]["medida"])
        arrayMedidas.append(medidaNova)

        collection.update_one({"sensorid": request["sensorid"]}, {"$set": { "medida": arrayMedidas}})

    print("[COLLECTION] done update!")

def populate_collection(collection):

    print("[COLLECTION] populating...")

    medida = {}

    for req in REQUESTS:
        
        request = REQUESTS[req]
        medida["timestamp"] = request["timestamp"]
        medida["bodytemp"] = request["bodytemp"]
        medida["bloodpress_systolic"] = request["bloodpress"]["systolic"]
        medida["bloodpress_diastolic"] = request["bloodpress"]["diastolic"]
        medida["bpm"] = request["bpm"]
        medida["sato2"] = request["sato2"]
    
        sensor_req = request
        del sensor_req["timestamp"]
        del sensor_req["bodytemp"]
        del sensor_req["bpm"]
        del sensor_req["sato2"]
        del sensor_req["bloodpress"]["systolic"]
        del sensor_req["bloodpress"]["diastolic"]
        del sensor_req["bloodpress"]

        sensor_req["medida"] = [medida]
        
        collection.insert_one(sensor_req)
 
    print("[COLLECTION] done populate!")

def connect_mongodb():
    global MDB_CLIENT
    MDB_CLIENT = MongoClient(cfg.mongodb_uri)

def load_api_to_dict():

    print("[API] Loading {} data...".format(cfg.base_api_url))
    
    range_min, range_max = 1, 6
    for req in range(range_min, range_max):
        url         = '{}{}{}'.format(cfg.base_api_url, 
                                      cfg.blood_api, req)
        request     = requests.get(url)
        jsonRequest = request.json()
        jsonString  = json.dumps(jsonRequest)
        jsonData    = json.loads(jsonString)
        REQUESTS[req] = jsonData
    
    print("[API] Loaded!")

if __name__ == '__main__':
    main()
