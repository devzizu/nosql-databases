
import os
import requests
import json
import config as cfg

from pymongo import MongoClient
from pprint import pprint

REQUESTS = {}

def main():

    os.system('cls' if os.name == 'nt' else 'clear')
    print("[SCRIPT] Starting...")

    #load_api_to_dict()

    connect_mongodb()
    global DB
    DB = MDB_CLIENT.example

    populate_collection()

    print("[SCRIPT] Finished!")

def populate_collection():
    global BLOOD
    try:
 
        DB.create_collection("Blood")
        
        print("Created collection Blood!")
           
    except Exception as msg:
        print("Failed to create collection:", msg, ", clearing collection...")
        BLOOD = DB["Blood"]

    BLOOD.drop()

    for req in REQUESTS:
        DB.Blood.insert(req)
 
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
