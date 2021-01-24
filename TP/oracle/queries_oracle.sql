/*Number of employees who work in Canada*/

select count(*) as "Number of employees who work in Canada" from countries c 
join locations l on c.country_id = l.country_id join departments d on 
l.location_id = d.location_id join employees e on 
d.department_id = e.department_id where country_name = 'Canada';

/*First and last name of the people whose actual job is Administration Vice 
President*/

select first_name, last_name from employees e join jobs j on e.job_id = j.job_id
where job_title = 'Administration Vice President';

/*Employees who had more than one job before*/

select e.first_name, e.last_name from employees e join job_history j on 
e.employee_id = j.employee_id group by e.first_name, e.last_name having
count(j.job_id)>1;

/*Department names and mean of its salaries with 2 decimal places*/

select department_name, round(avg(salary),2) as 
"Mean of the department's salaries" from departments d join employees e on 
d.department_id = e.department_id group by department_name;

/*ID and street address of the employees whose salary is higher than 10000*/

select employee_id, street_address from employees e join departments d on 
e.department_id = d.department_id join locations l on 
d.location_id = l.location_id where salary>10000;

/*Name of the region and number of departments of the region which has the
largest number of departments*/

select region_name, count(*) as "Number of departments" from regions r join 
countries c on r.region_id = c.region_id join locations l on 
l.country_id = c.country_id join departments d on 
d.location_id = l.location_id group by region_name order by 
"Number of departments" desc fetch first 1 rows only;

