
import cx_Oracle
import configparser
import csv

from pprint import pprint
from pymongo import MongoClient

def main():

    # read configuration file 
    setup_config("../configuration.toml")
    
    # create oracle connection
    if not create_oracle_connection():
        return
    # create global migrate data (EMP_JOB_REC)
    init_migrate_data()
    # close oracle connection
    close_oracle_connection()

    print("[run] done.")

def create_csv(filename, tablename):
    CURSOR.execute("select * from {}".format(tablename))
    with open(filename, 'w') as fout:
        writer = csv.writer(fout)
        writer.writerow([ i[0] for i in CURSOR.description ])
        writer.writerows(CURSOR.fetchall())

def init_migrate_data():
    
    print("[migrate-data] generating migrate documents...")

    global CURSOR
    CURSOR = ORA_CONN.cursor()
    
    tables = ["EMPLOYEES"]
    csv_folder = "gen_csv"

    for t in tables:
        create_csv("{}/{}.csv".format(csv_folder, t), t)

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
    if ORA_CONN:
        ORA_CONN.close()

def setup_config(path):
    
    print("[config] reading", path)
    global CONFIG
    CONFIG = configparser.ConfigParser()
    CONFIG.read(path)

if __name__ == '__main__':
    main()
