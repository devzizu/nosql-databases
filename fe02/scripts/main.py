import os, signal
import sys
import requests
import json
import cx_Oracle
import config
import sqlite3
import threading
import schedule
import time

from datetime import datetime
from sqlite3 import OperationalError

resultsDict          = {}
create_tables_file   = "../create_tables.sql"
drop_tables_file     = "../drop_tables.sql"
populate_tables_file = "../povoamento.sql"
update_medidas_file  = "../update.sql"
sql_insert           = "insert into TABLE values (VALUES);"
interval             = 5.0
execute_flag         = True

def handler(signum, frame):
    print("\nStopping the update process..., got sign = (SIGINT) ", signum)
    global execute_flag
    execute_flag = False

signal.signal(signal.SIGINT, handler)

def main():

    print("[RUN] Starting script...")

    os.system('cls' if os.name == 'nt' else 'clear')

    connection = connect_oracle()
    if connection == None:
        print("[ORACLE] Error connecting to oracleDB...")

    # Drop tables (if exists)
    load_sql_file(connection, drop_tables_file)
    # Create tables
    load_sql_file(connection, create_tables_file)

    # Load API
    load_api_to_dict()
    # Create file with sql commands (from api)
    load_datastructures_to_file(populate_tables_file)
    # Load sql file
    load_sql_file(connection, populate_tables_file)

    count_timer = 0
    while execute_flag:
        print("\n[RUN] Waiting...\n")
        time.sleep(interval)
        print("\n[RUN] Updating sensor values...\n")
        count_timer = update(count_timer, connection)
        load_sql_file(connection, update_medidas_file)

    print("[RUN] Script stopped...")

def update(count_timer, connection):
    count_timer+=interval
    load_api_to_dict()
    update_datastructures_to_file(update_medidas_file)
    print("\n\t(time elapsed +", count_timer, " s, intervals of ", interval, ")...\n")
    return count_timer

def update_datastructures_to_file(file_name):

    print("[GEN_SQL - UPDATE] Loading data structures...")

    f = open(file_name, "w")

    for key in resultsDict:

        medidas_val = "{}, {}, {}, {}, {}, {}, {}".format(
            "to_timestamp('{}', 'YYYY-MM-DD HH24:MI:SS')".format(resultsDict[key]["timestamp"]), \
            resultsDict[key]["sensorid"],
            resultsDict[key]["bodytemp"],
            resultsDict[key]["bloodpress"]["systolic"],
            resultsDict[key]["bloodpress"]["diastolic"],
            resultsDict[key]["bpm"],
            resultsDict[key]["sato2"]
        )
        
        sql_medidas = sql_insert.replace("TABLE", "medidas").replace("VALUES", medidas_val)

        f.write("{}\n".format(sql_medidas))

    f.close()

    print("[GEN_SQL - UPDATE] SQL file generated ('", populate_tables_file, "')...")

def load_datastructures_to_file(file_name):
    
    print("[GEN_SQL - POPULATE] Loading data structures...")

    f = open(file_name, "w")

    systemid = 1    
    careteamid = 1
    careteam_has_doctorid = 1

    for key in resultsDict:
        
        # Create only one system (for now)
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
            
            careteam_has_doctorid+=1

        patient_val = "{}, '{}', {}, {}".format( \
                    resultsDict[key]["patient"]["patientid"], \
                    resultsDict[key]["patient"]["patientname"], \
                    "to_date('{}', 'yyyy-mm-dd')" \
                    .format(datetime.strptime(resultsDict[key]["patient"]["patientbirthdate"], "%Y-%m-%d")).replace(" 00:00:00", ""), \
                    resultsDict[key]["patient"]["patientage"])

        sql_patient = sql_insert.replace("TABLE", "patient").replace("VALUES", patient_val)

        f.write("{}\n".format(sql_patient))

        sensor_val = "{}, {}, {}, {}, {}, {}, {}, {}, {}, {}" \
                .format(resultsDict[key]["sensorid"], \
                        careteamid, \
                        resultsDict[key]["patient"]["patientid"], \
                        systemid, \
                        resultsDict[key]["sensornum"], \
                        "'{}'".format(resultsDict[key]["type_of_sensor"]), \
                        "'{}'".format(resultsDict[key]["servicecod"]), \
                        "'{}'".format(resultsDict[key]["servicedesc"]), \
                        "to_date('{}', 'yyyy-mm-dd')".format(datetime.strptime(resultsDict[key]["admdate"], "%Y-%m-%d")).replace(" 00:00:00", ""), \
                        resultsDict[key]["bed"])
        sql_sensor = sql_insert.replace("TABLE", "sensor").replace("VALUES", sensor_val)

        medidas_val = "{}, {}, {}, {}, {}, {}, {}".format( \
            "to_timestamp('{}', 'YYYY-MM-DD HH24:MI:SS')".format(resultsDict[key]["timestamp"]), \
            resultsDict[key]["sensorid"], \
            resultsDict[key]["bodytemp"], \
            resultsDict[key]["bloodpress"]["systolic"], \
            resultsDict[key]["bloodpress"]["diastolic"], \
            resultsDict[key]["bpm"], \
            resultsDict[key]["sato2"]
        )
                
        sql_medidas = sql_insert.replace("TABLE", "medidas").replace("VALUES", medidas_val)

        f.write("{}\n".format(sql_sensor))
        f.write("{}\n".format(sql_medidas))

        careteamid+=1

    f.close()

    print("[GEN_SQL - POPULATE] SQL file generated ('", populate_tables_file, "')!")

def load_sql_file(connection, file_name):
    print("\n[SQL_QUERY] Loading sql file: {}".format(file_name))
    fd = open(file_name, 'r')
    sql_file = fd.read()
    fd.close()
    sql_commands = sql_file.split(";")
    for cmd in sql_commands:
        if len(cmd) < 2:
            continue
        cmd = cmd.replace("\n", "")
        print("\t[EXEC_SQL_QUERY] Executing sql statment (brief): '{}'".format(cmd[0:40]))
        try:
            with connection.cursor() as cursor:
                cursor.execute(cmd)
                connection.commit()
                print("\t\t(success)")
        except Exception as msg:
            print("\t\t(error) Last sql command Skipped, brief: ", msg, "!")
    
    print("[SQL_QUERY] SQL file loaded!")

def connect_oracle(): 
    try:
        print("\n[ORACLE] Connecting to OracleDB...")
        oracledb_connection = cx_Oracle.connect(
            config.ordb_username,
            config.ordb_password,
            config.ordb_dsn,
            encoding = config.ordb_encoding
        )
        print("\t{}".format(oracledb_connection))
        print("[ORACLE] Connection done!")
        
        return oracledb_connection;

    except cx_Oracle.Error as error:
        print("[ORACLE] Error while connecting to OracleDB (check error below):")
        print("(", error, ")")

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