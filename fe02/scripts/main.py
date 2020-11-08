"""
pip3 install requests
python3 -m pip install cx_Oracle --upgrade
"""

import os
import requests
import json
import cx_Oracle
import config
import sqlite3

from sqlite3 import OperationalError

#saves the api loaded
resultsDict = {}

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    connection = connect_oracle()
    load_sql_file(connection, "../create_tables.sql")

def load_tables(connection):
    print("\nLoading tables with data...")
    sql_example = 'insert into doctor values(1, \'Joaquim\')'
    with connection.cursor() as cursor:
        cursor.execute(sql_example)
        connection.commit()
        cursor.close()
    print("Tables loaded!")

def load_sql_file(connection, file_name):
    print("\nLoading sql file: {}".format(file_name))
    fd = open(file_name, 'r')
    sql_file = fd.read()
    fd.close()
    sql_commands = sql_file.split(";")
    for cmd in sql_commands:
        if len(cmd) < 2:
            continue
        cmd = cmd.replace("\n", "")
        print("Executing sql statment (brief): \"{} (...)\"".format(cmd[0:40]))
        try:
            with connection.cursor() as cursor:
                cursor.execute(cmd)
            print("\tSuccess!")
        except Exception as msg:
            print("\t\t(error) Last sql command Skipped...")
    print("SQL file loaded!")

def connect_oracle(): 
    try:
        print("\nConnecting to OracleDB...")
        oracledb_connection = cx_Oracle.connect(
            config.ordb_username,
            config.ordb_password,
            config.ordb_dsn,
            encoding = config.ordb_encoding
        )
        print("\t{}".format(oracledb_connection))
        print("Success!")
        
        return oracledb_connection;

    except cx_Oracle.Error as error:
        print("Error while connecting to OracleDB (check error below):")
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
        print("\nkey: {} -> value: \n\n{};".format(key, resultsDict[key]))

if __name__ == '__main__':
    main()
