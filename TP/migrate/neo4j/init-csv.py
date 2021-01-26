
import cx_Oracle
import configparser
import csv
import glob
import os
import shutil

from datetime import datetime
from pprint import pprint
from neo4j import GraphDatabase

GEN_CSV_FOLDER = "gen_csv"
INIT_SQL       = "init.sql"
EXPORT_FOLDER  = "/var/lib/neo4j/import/gen_csv"

def main():

    # read configuration file 
    setup_config("../configuration.toml")
    
    # create oracle connection
    if not create_oracle_connection():
        return
    # clear old csvs from GEN_CSV_FOLDER
    clear_folder(GEN_CSV_FOLDER)
    # parse sql statements form INIT_SQL file
    parse_generate_csv(INIT_SQL)

    # close oracle connection
    close_oracle_connection()
    
    # send to VM /var/lib
    export_csv(EXPORT_FOLDER)

    print("[run] done.")

def export_csv(dest):
    if (os.path.exists(dest)):
        shutil.rmtree(dest)
    print("[csv] exporting data to", dest)
    shutil.copytree(GEN_CSV_FOLDER, EXPORT_FOLDER)

def clear_folder(name):
    print("[os] clearing folder", name)
    if not (os.path.exists(name)):
        os.makedirs(name)
    else:
        files = glob.glob(name + "/*")
        for f in files:
            os.remove(f)

def parse_generate_csv(filename):
    print("[parser] parsing file", filename)
    global CURSOR
    CURSOR = ORA_CONN.cursor()

    fileD = open(filename, "r")
    Statements = fileD.readlines()

    EMP_RELATION = ""

    for line in Statements:
        # is empty line / comment   
        if not (len(line) == 0 or line.startswith("\n") or line.startswith("--")):
            parts = line.split("|")
            query = parts[0].replace("\n", "").replace(";", "")
            csv_file = parts[1].strip()
            if (csv_file.startswith("EMP_REL")):
                EMP_RELATION = query
            else:
                output_file = GEN_CSV_FOLDER + "/" + csv_file + ".csv"
                print("\t[csv] generating", output_file)
                create_csv(output_file, query)
    
    # manage employee relationship
    EMP_REL_ROWS = CURSOR.execute(EMP_RELATION).fetchall()

    OUTPUT = []

    LAST_EMPLOYEE = -1
    for row in EMP_REL_ROWS:
    
        RELATION = {}
        RELATION["EMPLOYEE_ID"] = row[0]
        
        # end date is null
        if not (row[5] is None):
            RELATION["END_DATE"]    = row[5].strftime("%Y.%m.%d")
        else:
            RELATION["END_DATE"] = "null"

        if (row[2] is None):

            # current job
            
            RELATION["JOB_ID"]        = row[1]
            RELATION["START_DATE"]    = row[3].strftime("%Y.%m.%d")
            RELATION["DEPARTMENT_ID"] = row[6]

        else:
            
            # previous job

            RELATION["JOB_ID"] = row[2]
            RELATION["START_DATE"] = row[4].strftime("%Y-%m-%d")
            RELATION["DEPARTMENT_ID"] = row[7]
        
            EXTRA = {}
            EXTRA["EMPLOYEE_ID"]   = row[0]
            EXTRA["END_DATE"]      = "null"
            EXTRA["JOB_ID"]        = row[1]
            EXTRA["START_DATE"]    = row[3].strftime("%Y-%m-%d")
            EXTRA["DEPARTMENT_ID"] = row[6]
            
            if not (LAST_EMPLOYEE == row[0]):
                OUTPUT.append(EXTRA)

        LAST_EMPLOYEE = row[0]
        
        OUTPUT.append(RELATION)

    csv_out = GEN_CSV_FOLDER + "/employees_relationship.csv"
    print("\t[csv] generating", csv_out)
    
    header = OUTPUT[0].keys()
    
    with open(csv_out, 'w', newline='') as output_file:
        dWriter = csv.DictWriter(output_file, header)
        dWriter.writeheader()
        dWriter.writerows(OUTPUT)

def create_csv(filename, query):
    CURSOR.execute(query)
    with open(filename, 'w') as fout:
        writer = csv.writer(fout)
        writer.writerow([ i[0] for i in CURSOR.description ])
        try:
            resultSet = CURSOR.fetchall()
            writer.writerows(resultSet)
        except cx_Oracle.DatabaseError as e:
            raise

def create_oracle_connection():
    print("[oracle] creating connection, status = ", end="")
    host  = CONFIG['oracle']['host']
    port  = CONFIG['oracle']['port']
    sname = CONFIG['oracle']['service']
    dsn  = cx_Oracle.makedsn(host, port, service_name=sname)
    global ORA_CONN
    try:
        ORA_CONN = cx_Oracle.connect(
            CONFIG['oracle']['user'],
            CONFIG['oracle']['passwd'],
            dsn,
            encoding = CONFIG['oracle']['encoding']
        )
    
        print("ok, version: ", ORA_CONN.version)
    
    except cx_Oracle.Error as error:
        print("error (is your database disconnected?)")
        return False

    return True

def close_oracle_connection():
    print("[oracle] closing connection")
    if ORA_CONN:
        ORA_CONN.close()

def setup_config(path):
    
    print("[config] reading", path)
    global CONFIG
    CONFIG = configparser.ConfigParser()
    CONFIG.read(path)

if __name__ == '__main__':
    main()
