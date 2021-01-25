
import cx_Oracle
import configparser
import csv
import glob
import os

from pprint import pprint
from neo4j import GraphDatabase

GEN_CSV_FOLDER = "gen_csv"
INIT_SQL       = "init.sql"

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
    send_csv_vm()

    print("[run] done.")

def send_csv_vm():
    print("[vm] exporting data to vm...")
    host   = CONFIG['vm']['host']
    user   = CONFIG['vm']['user']
    passwd = CONFIG['vm']['passwd']

    cmd = "sshpass -p '{}' scp -P 2222 -r {}/ {}@{}:/var/lib/neo4j/import".format(passwd, GEN_CSV_FOLDER,user, host)
    os.system(cmd)

def clear_folder(name):
    print("[os] clearing folder", name)
    files = glob.glob(name + "/*")
    for f in files:
        os.remove(f)

def parse_generate_csv(filename):
    print("[parser] parsing file", filename)
    global CURSOR
    CURSOR = ORA_CONN.cursor()

    fileD = open(filename, "r")
    Statements = fileD.readlines()

    EMP_REL_1, EMP_REL_2 = "", ""

    for line in Statements:
        # is empty line / comment   
        if not (len(line) == 0 or line.startswith("\n") or line.startswith("--")):
            parts = line.split("|")
            query = parts[0].replace("\n", "").replace(";", "")
            csv_file = parts[1].strip()
            output_file = GEN_CSV_FOLDER + "/" + csv_file + ".csv"
            print("\t[csv] generating", output_file)
            create_csv(output_file, query)
    
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
