--Export the following results with Export Wizard to generate the csv files

--countries.csv
select country_id, country_name from countries;

--countries_locations.csv
select location_id, country_id from locations;

--countries_regions.csv
select country_id, region_id from countries;

--departments.csv
select department_id, department_name from departments;

--departments_locations.csv
select department_id, location_id from departments;

--departments_managers.csv
select department_id, manager_id from departments;

--employees_departments.csv
select employee_id, department_id from employees;

--employees_managers.csv
select employee_id, manager_id from employees;

--employees.csv (careful with the commas)
select employee_id, first_name, last_name, email, phone_number, salary, 
commission_pct from employees;

--jobs.csv
select * from jobs;

--locations.csv
select location_id, street_address, postal_code, city, state_province from 
locations;

--regions.csv
select * from regions;

--employees_relationship.csv (join the results into one)
ALTER TABLE employees ADD END_DATE DATE;

select employee_id, job_id, hire_date as "START_DATE", end_date from employees;

select employee_id, job_id, start_date, end_date from job_history;