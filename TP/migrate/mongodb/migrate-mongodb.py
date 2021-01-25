
import cx_Oracle
import configparser

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

    # create mongodb client 
    init_mongodb_migrate()    
    # migrate generated data
    migrate_documents()

    print("[run] done.")

def migrate_documents():
    for record in EMP_JOB_REC:
        employeesCollection.insert_one(record)

def init_mongodb_migrate():

    print("[mongodb] setting up connection, status = ", end = "")
    global MDB_CLIENT
    MDB_CLIENT = MongoClient(CONFIG['mongodb']['uri'])
    print("ok", MDB_CLIENT.server_info()['ok'])

    global HR_DB
    HR_DB = MDB_CLIENT.hr_migrate

    global employeesCollection
    # create/switch collection
    employeesCollection = HR_DB.employees
    # clear all documents
    employeesCollection.delete_many({})

def init_migrate_data():
    
    print("[migrate-data] generating migrate documents...")

    global EMP_JOB_REC
    EMP_JOB_REC = []
 
    cursor = ORA_CONN.cursor()

    # get all employees
    cursor.execute("select * from EMPLOYEES")
    employeesRows = dict(map(lambda row: (row[0], row), cursor.fetchall()))

    # get all jobs
    cursor.execute("select * from JOBS")
    jobsRows = dict(map(lambda row: (row[0], row), cursor.fetchall()))
    
    # get all job_history
    cursor.execute("select * from JOB_HISTORY")
    jobHistoryRows = cursor.fetchall()
 
    # get all departments
    cursor.execute("select * from DEPARTMENTS")
    departmentRows = dict(map(lambda row: (row[0], row), cursor.fetchall()))

    # get all locations
    cursor.execute("select * from LOCATIONS")
    locationRows = dict(map(lambda row: (row[0], row), cursor.fetchall()))

    # get all countries
    cursor.execute("select * from COUNTRIES")
    countriesRows = dict(map(lambda row: (row[0], row), cursor.fetchall()))

    # get all locations
    cursor.execute("select * from REGIONS")
    regionsRows = dict(map(lambda row: (row[0], row), cursor.fetchall()))

    for jb in jobsRows.values():

        job_id         = jb[0]
        
        for emp in employeesRows.values():

            EMP_RECORD = {}
            
            emp_id = emp[0]
            
            # Parse current job information

            EMP_RECORD["job_title"]      = jb[1] 
            EMP_RECORD["job_min_salary"] = jb[2] 
            EMP_RECORD["job_max_salary"] = jb[3] 

            if job_id != emp[6]:
                continue

            EMP_RECORD["first_name"]    = emp[1]
            EMP_RECORD["last_name"]     = emp[2]
            EMP_RECORD["email"]         = emp[3]
            EMP_RECORD["phone_number"]  = emp[4]
            EMP_RECORD["hire_date"]     = emp[5].strftime("%d-%m-%Y")
            EMP_RECORD["salary"]        = emp[7]
            EMP_RECORD["comission_pct"] = emp[8]
            emp_depart_id  = emp[10]
            
            # Parse current department information

            if not (emp_depart_id is None):
                EMP_RECORD["curr_dep_manager_email"] = employeesRows[departmentRows[emp_depart_id][2]][3]
                EMP_RECORD["curr_dep_name"]          = departmentRows[emp_depart_id][1]             
                dep_atual_locat_id                   = departmentRows[emp_depart_id][3]                           
                EMP_RECORD["curr_dep_loc_st_addr"]   = locationRows[dep_atual_locat_id][1] 
                EMP_RECORD["curr_dep_loc_pt_code"]   = locationRows[dep_atual_locat_id][2] 
                EMP_RECORD["curr_dep_loc_city"]      = locationRows[dep_atual_locat_id][3] 
                EMP_RECORD["curr_dep_loc_st_prov"]   = locationRows[dep_atual_locat_id][4] 
                dep_atual_count_id                   = locationRows[dep_atual_locat_id][5]

                if not (dep_atual_count_id is None):
                    EMP_RECORD["curr_dep_country_name"] = countriesRows[dep_atual_count_id][1]
                    count_atual_reg_id                   = countriesRows[dep_atual_count_id][2]

                    if not (count_atual_reg_id is None):
                        EMP_RECORD["curr_dep_region_name"] = regionsRows[count_atual_reg_id][1]

            # Parse job history rows
        
            EMP_RECORD["hist"] = []

            for jb_hist in jobHistoryRows:
                
                if (jb_hist[0] == emp_id):

                    TMP_EMP_RECORD = {}

                    TMP_EMP_RECORD["hist_start_date"] = jb_hist[1].strftime("%d-%m-%Y")
                    TMP_EMP_RECORD["hist_end_date"]   = jb_hist[2].strftime("%d-%m-%Y")
                    TMP_EMP_RECORD["hist_job_title"]  = jobsRows[jb_hist[3]][1]
                    hist_depart_id                    = jb_hist[4]
                    
                    if not (hist_depart_id is None):
                        
                        TMP_EMP_RECORD["hist_dep_name"]          = departmentRows[hist_depart_id][1]             
                        dep_hist_locat_id                        = departmentRows[hist_depart_id][3]                           
                        TMP_EMP_RECORD["hist_dep_loc_st_addr"]   = locationRows[dep_hist_locat_id][1] 
                        TMP_EMP_RECORD["hist_dep_loc_pt_code"]   = locationRows[dep_hist_locat_id][2] 
                        TMP_EMP_RECORD["hist_dep_loc_city"]      = locationRows[dep_hist_locat_id][3] 
                        TMP_EMP_RECORD["hist_dep_loc_st_prov"]   = locationRows[dep_hist_locat_id][4] 
                        dep_hist_count_id                        = locationRows[dep_hist_locat_id][5]

                        if not (dep_hist_count_id is None):
                            TMP_EMP_RECORD["hist_dep_country_name"] = countriesRows[dep_hist_count_id][1]
                            count_hist_reg_id                       = countriesRows[dep_hist_count_id][2]

                            if not (count_hist_reg_id is None):
                                TMP_EMP_RECORD["hist_dep_region_name"] = regionsRows[count_hist_reg_id][1]

    
                    EMP_RECORD["hist"].append(TMP_EMP_RECORD)                

            EMP_JOB_REC.append(EMP_RECORD)    
    
    print("[migrate-data] all data was generated.")

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
