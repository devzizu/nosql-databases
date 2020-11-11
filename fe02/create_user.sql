create tablespace health_tables datafile 'health_files_01.dbf' size 500m;

create user health identified by "newpassword" default tablespace health_tables
quota unlimited on health_tables;

grant connect, resource, create view, create sequence to health;