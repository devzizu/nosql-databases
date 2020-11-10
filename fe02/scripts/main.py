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

from datetime import datetime
from sqlite3 import OperationalError

#saves the api loaded
resultsDict = {}

sql_insert = "insert into TABLE values (VALUES);"

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    connection = connect_oracle()
    #load_sql_file(connection, "../create_tables.sql")
    load_api_to_dict()
    load_datastructures_to_file("../povoamento.sql")
    load_sql_file(connection, "../povoamento.sql")

def load_datastructures_to_file(file_name):

    f = open(file_name, "w")

    systemid = 1    
    careteamid = 1
    careteam_has_doctorid = 1

    for key in resultsDict:

        if careteamid == 1:
            system_val = "{}, {}".format(systemid, resultsDict[key]["number_of_sensors"])

        sql_system = sql_insert.replace("TABLE", "system").replace("VALUES", system_val)
        f.write("{}\n".format(sql_system))

        careteam_val = "{}".format(careteamid)
        sql_careteam = sql_insert.replace("TABLE", "careteam").replace("VALUES", careteam_val)

        f.write("{}\n".format(sql_careteam))

        for doc in resultsDict[key]["careteam"]:

            doctor_val = "{}, '{}'".format(doc["id"], doc["nome"])
            sql_doc = sql_insert.replace("TABLE", "doctor").replace("VALUES", doctor_val)

            f.write("{}\n".format(sql_doc))

            careteam_has_doctor_val = "{}, {}, {}".format( \
                careteam_has_doctorid, \
                careteamid, \
                doc["id"]
            )

            sql_careteam_has_doctor = sql_insert.replace("TABLE", "careteam_has_doctor").replace("VALUES", careteam_has_doctor_val)

            f.write("{}\n".format(sql_careteam_has_doctor))

        patient_val = "{}, '{}', {}, {}".format( \
                    resultsDict[key]["patient"]["patientid"], \
                    resultsDict[key]["patient"]["patientname"], \
                    "to_date('{}', 'yyyy-mm-dd')" \
                    .format(datetime.strptime(resultsDict[key]["patient"]["patientbirthdate"], "%Y-%m-%d")).replace(" 00:00:00", ""), \
                    resultsDict[key]["patient"]["patientage"])

        sql_patient = sql_insert.replace("TABLE", "patient").replace("VALUES", patient_val)

        f.write("{}\n".format(sql_patient))

        sensor_val = "{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}" \
                .format(resultsDict[key]["sensorid"], \
                        careteamid, \
                        resultsDict[key]["patient"]["patientid"], \
                        systemid, \
                        resultsDict[key]["sensornum"], \
                        "'{}'".format(resultsDict[key]["type_of_sensor"]), \
                        "'{}'".format(resultsDict[key]["servicecod"]), \
                        "'{}'".format(resultsDict[key]["servicedesc"]), \
                        "to_date('{}', 'yyyy-mm-dd')".format(datetime.strptime(resultsDict[key]["admdate"], "%Y-%m-%d")).replace(" 00:00:00", ""), \
                        resultsDict[key]["bed"], \
                        resultsDict[key]["bodytemp"], \
                        resultsDict[key]["bloodpress"]["systolic"], \
                        resultsDict[key]["bloodpress"]["diastolic"], \
                        resultsDict[key]["bpm"], \
                        resultsDict[key]["sato2"], \
                        resultsDict[key]["timestamp"])
        sql_sensor = sql_insert.replace("TABLE", "sensor").replace("VALUES", sensor_val)

        f.write("{}\n".format(sql_sensor))


        careteamid+=1
        careteam_has_doctorid+=1

    f.close()

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
        print("Executing sql statment (brief): '{}'".format(cmd[0:40]))
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
    print("Loading API data...")
    range_min_sensor, range_max_sensor = 1, 6
    for requestID in range(range_min_sensor, range_max_sensor):
        url         = '{}{}{}'.format(config.base_api_url, config.sensor_api, requestID)
        request     = requests.get(url)
        jsonRequest = request.json()
        jsonString  = json.dumps(jsonRequest)
        jsonData    = json.loads(jsonString)
        resultsDict[requestID] = jsonData

if __name__ == '__main__':
    main()
