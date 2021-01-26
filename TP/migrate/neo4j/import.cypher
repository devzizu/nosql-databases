//remove all
match (n) detach delete n

//import countries
LOAD CSV WITH HEADERS FROM 'file:///gen_csv/countries.csv' AS line
CREATE (:Country { country_id: line.COUNTRY_ID, country_name: line.COUNTRY_NAME})

//import regions
LOAD CSV WITH HEADERS FROM 'file:///gen_csv/regions.csv' AS line
CREATE (:Region { region_id: line.REGION_ID, region_name: line.REGION_NAME})

//import locations
LOAD CSV WITH HEADERS FROM 'file:///gen_csv/locations.csv' AS line
CREATE (:Location { location_id: line.LOCATION_ID, street_address: line.STREET_ADDRESS, postal_code: line.POSTAL_CODE, city: line.CITY, state_province: line.STATE_PROVINCE})

//import departments
LOAD CSV WITH HEADERS FROM 'file:///gen_csv/departments.csv' AS line
CREATE (:Department { department_id: line.DEPARTMENT_ID, department_name: line.DEPARTMENT_NAME})

//import jobs
LOAD CSV WITH HEADERS FROM 'file:///gen_csv/jobs.csv' AS line
CREATE (:Job { job_id: line.JOB_ID, job_title: line.JOB_TITLE, job_min_salary: line.MIN_SALARY, job_max_salary: line.MAX_SALARY})

//import employees
LOAD CSV WITH HEADERS FROM 'file:///gen_csv/employees.csv' AS line FIELDTERMINATOR ','
CREATE (:Employee { employee_id: line.EMPLOYEE_ID, employee_first_name: line.FIRST_NAME, employee_last_name: line.LAST_NAME, employee_email: line.EMAIL, employee_phone_number: line.PHONE_NUMBER, employee_salary: line.SALARY, employee_commission_pct: line.COMMISSION_PCT})

//import relationship between country and region
LOAD CSV WITH HEADERS FROM "file:///gen_csv/countries_regions.csv" AS row
MATCH (c:Country {country_id:row.COUNTRY_ID}), (r:Region {region_id:row.REGION_ID})
CREATE (c)-[:SITUADO_EM]->(r);

//import relationship between country and location
LOAD CSV WITH HEADERS FROM "file:///gen_csv/countries_locations.csv" AS row
MATCH (c:Country {country_id:row.COUNTRY_ID}), (l:Location {location_id:row.LOCATION_ID})
CREATE (l)-[:PERTENCE_A]->(c);

//import relationship between department and location
LOAD CSV WITH HEADERS FROM "file:///gen_csv/departments_locations.csv" AS row
MATCH (d:Department {department_id:row.DEPARTMENT_ID}), (l:Location {location_id:row.LOCATION_ID})
CREATE (d)-[:LOCALIZADO_EM]->(l);

//import relationship between employee and manager
LOAD CSV WITH HEADERS FROM "file:///gen_csv/employees_managers.csv" AS row
MATCH (e1:Employee {employee_id:row.EMPLOYEE_ID}), (e2:Employee {employee_id:row.MANAGER_ID})
CREATE (e1)-[:GERIDO_POR]->(e2);

//import relationship between department and manager
LOAD CSV WITH HEADERS FROM "file:///gen_csv/departments_managers.csv" AS row
MATCH (d:Department {department_id:row.DEPARTMENT_ID}), (e:Employee {employee_id:row.MANAGER_ID})
CREATE (e)-[:GERE]->(d);

//import relationship between department and employee
LOAD CSV WITH HEADERS FROM "file:///gen_csv/employees_departments.csv" AS row
MATCH (d:Department {department_id:row.DEPARTMENT_ID}), (e:Employee {employee_id:row.EMPLOYEE_ID})
CREATE (d)-[:POSSUI]->(e);

//import relationship between employee and job
LOAD CSV WITH HEADERS FROM "file:///gen_csv/employees_relationship.csv" AS csvLine
MATCH (e:Employee {employee_id: csvLine.EMPLOYEE_ID}),(j:Job {job_id: csvLine.JOB_ID})
CREATE (e)-[:DESEMPENHA {start_date: csvLine.START_DATE, end_date: csvLine.END_DATE, department_id: csvLine.DEPARTMENT_ID}]->(j);

