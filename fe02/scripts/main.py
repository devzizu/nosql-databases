"""
pip3 install requests
python3 -m pip install cx_Oracle --upgrade
"""

import requests
import json
import cx_Oracle
import config

#oracle db connection
oracledb    = None
#saves the api loaded
resultsDict = {}

def connect_oracle(): 
    try:
        print("Connecting to OracleDB...")
        oracledb = cx_Oracle.connect(
            config.ordb_username,
            config.ordb_password,
            config.ordb_dsn,
            encoding = config.ordb_encoding
        )
        print("Connected...")
        
        sql = 'insert into doctor values(1, \'Joaquim\')'
        with oracledb.cursor() as cursor:
            cursor.execute(sql)
            oracledb.commit()
    
    except cx_Oracle.Error as error:
        print(error)


def load_api_to_dict():
    range_min_sensor, range_max_sensor = 1, 6
    for requestID in range(range_min_sensor, range_max_sensor):
        url         = '{}{}{}'.format(config.base_api_url, config.sensor_api, requestID)
        request     = requests.get(url)
        jsonRequest = request.json()
        jsonString  = json.dumps(jsonRequest)
        jsonData    = json.loads(jsonString)
        resultsDict[requestID] = jsonData

    for key in resultsDict:
        print("\nkey: {} -> value: \n\n{};".format(key, resultsDict[key]['timestamp']))

connect_oracle()
#load_api_to_dict()
