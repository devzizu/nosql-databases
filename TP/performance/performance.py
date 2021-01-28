
import cx_Oracle
import configparser
import time
import os
import shutil
import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from pprint import pprint
from pymongo import MongoClient
from neo4j import GraphDatabase

QUERIES_FOLDER  = "../queries"
QUERIES_ORACLE  = "queries_oracle.sql"
QUERIES_MONGODB = "queries.mongodb" 
QUERIES_CYPHER  = "queries_neo4j.cypher"  

# output csv folder
OUTPUT_FOLDER   = "results"
# number of tests for each query
NUMBER_EXEC     = 20
# multiply nanoseconds by factor
FACTOR = pow(10,6)
# round n decimal places
ROUND = 6

def main():

    # read configuration file 
    setup_config("../migrate/configuration.toml")
    
    create_folder(OUTPUT_FOLDER)
    
    # create connections
    if not create_oracle_connection():
        return
    create_neo4j_connection()



    # run performance tests

    performance_oracle(QUERIES_FOLDER + "/" + QUERIES_ORACLE)
    performance_neo4j(QUERIES_FOLDER + "/" + QUERIES_CYPHER)

    #plot_all()



    # close connections
    close_neo4j_connection
    close_oracle_connection()

    print("[run] done.")

def performance_neo4j(queries_file):

    print("[neo4j] performing tests for cypher queries...")

    queries = []

    lines = open(queries_file, "r").readlines()
    AcumLine = ""
    ParsedLines = []
    with NEO4J_CLIENT.session() as graphDB_Session:
        for line in lines:
            # if its not comment
            if (line.startswith("\n")):
                ParsedLines.append(AcumLine)
                AcumLine = ""
            if not (line.startswith("/*") or len(line) == 0):
                AcumLine = AcumLine + line
    
    for query in ParsedLines:
        if len(query) > 1:
            print("----------------------------------------------------------")
            print(query)
            graphDB_Session.run(query)

"""
    TESTS_MAP = {}

    queryid = 0
    for query in queries:

        queryE = "query{}".format(queryid)
        TESTS_MAP[queryE] = []

        for testid in range(0, NUMBER_EXEC):
            start = time.process_time()
            CURSOR.execute(query).fetchall()
            end   = time.process_time() - start
            TESTS_MAP[queryE].append(round(end * FACTOR, ROUND))

        values = TESTS_MAP[queryE]
        avg = round((sum(values)/ len(values)), ROUND)
        print("[query-{}] {} executions, average time = {}".format(queryid, NUMBER_EXEC, avg))
        filename = "{}/oracle-query{}.csv".format(OUTPUT_FOLDER, queryid)
        create_csv(TESTS_MAP[queryE], filename)
        queryid = queryid + 1
"""

def performance_oracle(queries_file):

    print("[oracle] performing tests for oracle queries...")

    CURSOR = ORA_CONN.cursor()

    queries = []

    for line in open(queries_file, "r").readlines():
        if not (line.startswith("/*") or line.startswith("\n") or len(line) == 0):
            queries.append(line.replace(";",""))    

    TESTS_MAP = {}

    queryid = 0
    for query in queries:

        queryE = "query{}".format(queryid)
        TESTS_MAP[queryE] = []

        for testid in range(0, NUMBER_EXEC):
            start = time.process_time()
            CURSOR.execute(query).fetchall()
            end   = time.process_time() - start
            TESTS_MAP[queryE].append(round(end * FACTOR, ROUND))

        values = TESTS_MAP[queryE]
        avg = round((sum(values)/ len(values)), ROUND)
        print("[query-{}] {} executions, average time = {}".format(queryid, NUMBER_EXEC, avg))
        filename = "{}/oracle-query{}.csv".format(OUTPUT_FOLDER, queryid)
        create_csv(TESTS_MAP[queryE], filename)
        queryid = queryid + 1

def plot_csv(x, y, db):

    for qid in range(0, 6):   
        query = "query{}".format(qid)
        df = pd.read_csv("results/{}-{}.csv".format(db, query))
        axs[x,y].plot(df["test#"], df["time"], label=query)

    axs[0,0].set_title("dbms: {}".format(db))


def plot_all():

    global axs, fig
    fig, axs = plt.subplots(2,2, figsize=(15, 15))

    plt.setp(axs, xticks=np.arange(0,NUMBER_EXEC,2).tolist())

    for ax in axs.flat:
        ax.set(xlabel="Execution ID", ylabel="Time (ms)")
    
    # view plots for each dbms

    plot_csv(0, 0, "oracle")
    
    

    # display subplots

    plt.legend(loc="upper right")
    plt.show()

def create_folder(folder):
    print("[os] clearing folder", folder)
    if (os.path.exists(folder)):
        shutil.rmtree(folder)
    os.mkdir(folder)


def create_csv(vals, filename):
    
    with open(filename, 'w') as f:
        w = csv.writer(f)
        w.writerow(["test#", "time"])
        vid = 0
        for v in vals:
            w.writerow([vid, v])
            vid = vid + 1

def create_neo4j_connection():
    uri    = CONFIG['neo4j']['uri'] 
    user   = CONFIG['neo4j']['user'] 
    passwd = CONFIG['neo4j']['passwd'] 
    
    print("[neo4j] connecting to", uri)
    
    global NEO4J_CLIENT
    NEO4J_CLIENT = GraphDatabase.driver(uri, auth=(user, passwd))

def close_neo4j_connection():
    print("[neo4j] close connection...")
    NEO4J_CLIENT.close()

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
    print("[oracle] closing connection...")
    if ORA_CONN:
        ORA_CONN.close()

def setup_config(path):
    
    print("[config] reading", path)
    global CONFIG
    CONFIG = configparser.ConfigParser()
    CONFIG.read(path)

if __name__ == '__main__':
    main()
