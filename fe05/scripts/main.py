import os, signal
import requests
import json
from pprint import pprint

resultsDict = {}
urlApi = "http://nosql.hpeixoto.me/api/sensor_elastic/400"
urlElastic = "http://localhost:9200/sensor400"
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

def main():

    print("[RUN] Starting script...")

    os.system('cls' if os.name == 'nt' else 'clear')

    for rID in range(1, 10):
        load_api_to_dict()
        for result in resultsDict:
            urlPOST = "{}{}/_doc".format(urlElastic, result)
            print(urlPOST)
            x = requests.post(urlPOST, data=json.dumps(resultsDict[result]), headers=headers)
        print("\n-> Request #",rID,"\n")
            

    print("[RUN] Script stopped...")

def load_api_to_dict():
    print("Loading API data...")
    range_min_sensor, range_max_sensor = 1, 6
    for requestID in range(range_min_sensor, range_max_sensor):
        url         = '{}{}'.format(urlApi, requestID)
        request     = requests.get(url)
        jsonRequest = request.json()
        jsonString  = json.dumps(jsonRequest)
        jsonData    = json.loads(jsonString)
        resultsDict[requestID] = jsonData

if __name__ == '__main__':
    main()
