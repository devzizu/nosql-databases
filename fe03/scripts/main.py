
import time
import os
import requests
import json
import config as cfg

from pymongo import MongoClient
from pprint import pprint

time_sleep = 6

def main():

    os.system('cls' if os.name == 'nt' else 'clear')
    print("[SCRIPT] Starting...")

    cardiacAPI = load_api_to_dict(cfg.cardiac_api)
    bloodAPI   = load_api_to_dict(cfg.blood_api)

    connect_mongodb()
    global DB
    DB = MDB_CLIENT.ficha3

    # create/switch to collection
    sensorCollection = DB.sensor

    # clear all documents
    sensorCollection.delete_many({})

    populate_collection(sensorCollection, cardiacAPI)
    populate_collection(sensorCollection, bloodAPI)
    

    while True:
        print("[SCRIPT] sleeping... (+", time_sleep,"s)")
        time.sleep(time_sleep)

        cardiacAPI = load_api_to_dict(cfg.cardiac_api)
        bloodAPI   = load_api_to_dict(cfg.blood_api)

        populate_collection(sensorCollection, cardiacAPI)
        populate_collection(sensorCollection, bloodAPI)

    print("[SCRIPT] Finished!")

def populate_collection(collection, reqs):

    print("[COLLECTION] populating...")

    medida = {}

    for req in reqs:
        request = reqs[req]
        collection.insert_one(request)
 
    print("[COLLECTION] done populate!")

def connect_mongodb():
    global MDB_CLIENT
    MDB_CLIENT = MongoClient(cfg.mongodb_uri)

def load_api_to_dict(api):

    REQUESTS = {}

    print("[API] Loading {} data... ({})".format(cfg.base_api_url, api))
    
    range_min, range_max = 1, 6
    for req in range(range_min, range_max):
        url         = '{}{}{}'.format(cfg.base_api_url, 
                                      api, req)
        request     = requests.get(url)
        jsonRequest = request.json()
        jsonString  = json.dumps(jsonRequest)
        jsonData    = json.loads(jsonString)
        REQUESTS[req] = jsonData
    
    return REQUESTS

    print("[API] Loaded!")

if __name__ == '__main__':
    main()
