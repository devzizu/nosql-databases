//import countries
LOAD CSV WITH HEADERS FROM 'file:///countries.csv' AS line
CREATE (:Country { country_id: line.COUNTRY_ID, country_name: line.COUNTRY_NAME})

//import regions
LOAD CSV WITH HEADERS FROM 'file:///regions.csv' AS line
CREATE (:Region { region_id: line.REGION_ID, region_name: line.REGION_NAME})

//import locations
LOAD CSV WITH HEADERS FROM 'file:///locations.csv' AS line
CREATE (:Location { location_id: line.LOCATION_ID, street_address: line.STREET_ADDRESS, postal_code: line.POSTAL_CODE, city: line.CITY, state_province: line.STATE_PROVINCE})

//import relationship between country and region
LOAD CSV WITH HEADERS FROM "file:///countries_regions.csv" AS row
MATCH (c:Country {country_id:row.COUNTRY_ID}), (r:Region {region_id:row.REGION_ID})
CREATE (c)-[:PERTENCE_A]->(r);

//import relationship between country and location
LOAD CSV WITH HEADERS FROM "file:///countries_locations.csv" AS row
MATCH (c:Country {country_id:row.COUNTRY_ID}), (l:Location {location_id:row.LOCATION_ID})
CREATE (l)-[:PERTENCE_A]->(c);

//import departments
LOAD CSV WITH HEADERS FROM 'file:///departments.csv' AS line
CREATE (:Department { department_id: line.DEPARTMENT_ID, department_name: line.DEPARTMENT_NAME})

//import relationship between department and location
LOAD CSV WITH HEADERS FROM "file:///departments_locations.csv" AS row
MATCH (d:Department {department_id:row.DEPARTMENT_ID}), (l:Location {location_id:row.LOCATION_ID})
CREATE (d)-[:LOCALIZADO_EM]->(l);
