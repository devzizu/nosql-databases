
import configparser
import csv

from pprint import pprint
from neo4j import GraphDatabase

GEN_CSV_FOLDER = "gen_csv"
IMPORT_CYPHER  = "import.cypher"

def main():

    # read configuration file 
    setup_config("../configuration.toml")
    
    # create neo4j connection
    create_neo4j_connection()
    # migrate neo4j data
    migrate_neo4j()
    # close neo4j connection
    close_neo4j_connection()

    print("[run] done.")

def migrate_neo4j():
        
    fd = open(IMPORT_CYPHER, "r")
    lines = fd.readlines()

    AcumLine = ""
    ParsedLines = []
    with NEO4J_CLIENT.session() as graphDB_Session:
        for line in lines:
            # if its not comment
            if (line.startswith("\n")):
                ParsedLines.append(AcumLine)
                AcumLine = ""
            if not (line.startswith("//") or len(line) == 0):
                AcumLine = AcumLine + line

        for query in ParsedLines:
            graphDB_Session.run(query)

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

def setup_config(path):
    
    print("[config] reading", path)
    global CONFIG
    CONFIG = configparser.ConfigParser()
    CONFIG.read(path)

if __name__ == '__main__':
    main()
