/*Number of employees who work in Canada*/

match (c:Country)<-[:PERTENCE_A]-(l:Location)<-[:LOCALIZADO_EM]-(d:Department)
-[:POSSUI]->(e:Employee) where c.country_name='Canada' return count(e) as 
`Number of employees who work in Canada`

/*First and last name of the people whose actual job is Administration Vice President*/

match (e:Employee)-[d:DESEMPENHA]->(j:Job) where d.end_date is NULL and 
j.job_title='Administration Vice President' return e.employee_first_name,
e.employee_last_name

/*Employees who had more than one job before*/

match (e:Employee)-[d:DESEMPENHA]->(j:Job) where d.end_date is not null
with e.employee_first_name as first_name, e.employee_last_name as last_name, 
count(*) as n_jobs where n_jobs > 1 return first_name, last_name

/*Department names and mean of its salaries with 2 decimal places*/

match (e:Employee)<-[:POSSUI]-(d:Department) return d.department_name
, round(10^2*avg(toInteger(e.employee_salary)))/10^2 as `Mean of the 
department's salaries`

/*ID and street address of the employees whose salary is higher than 10000*/

match (l:Location)<-[:LOCALIZADO_EM]-(d:Department)-[:POSSUI]->(e:Employee) 
where toInteger(e.employee_salary)>10000 return e.employee_id,l.street_address

/*Name of the region and number of departments of the region which has the largest number of departments*/

match (r:Region)<-[:SITUADO_EM]-(c:Country)<-[:PERTENCE_A]-(l:Location)
<-[:LOCALIZADO_EM]-(d:Department) return r.region_name, count(d) as 
`Number of departments` order by count(d) desc limit 1


/* Extra - Demonstrações */
/*match (dep:Department) with dep as Departs match (e:Employee) -[d:DESEMPENHA]->(j:Job) where e.employee_id = "101" and d.department_id in Departs.department_id and d.end_date <> "null" return Departs*/
