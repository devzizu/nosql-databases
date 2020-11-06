CREATE TABLE doctor
(
	doctorid int NOT NULL ENABLE,
	name VARCHAR2(45 byte),
	CONSTRAINT DOCTOR_PK PRIMARY KEY (doctorid)
);

CREATE TABLE patient
(
	patientid int NOT NULL ENABLE,
	patientname VARCHAR2(45 byte),
	patientbirthdate DATE,
	patientage int,
	CONSTRAINT PATIENT_PK PRIMARY KEY (patientid)
);

CREATE TABLE system
(
	systemid int NOT NULL ENABLE,
    number_of_sensors int,
    CONSTRAINT SYSTEM_PK PRIMARY KEY (systemid)
);

create table careteam
(
	careteamid int not null enable,
	constraint CARETEAM_PK primary key (careteamid)
);

CREATE TABLE careteam_has_doctor
(
	careteam_has_doctorid int NOT NULL ENABLE,
    careteamid int not null enable,
    doctorid int not null enable,
	constraint CARETEAM_HAS_DOCTOR_PK primary key(careteam_has_doctorid),
	constraint CARETEAM_FK foreign key(careteamid) references careteam(careteamid) enable,
	constraint DOCTOR_FK foreign key(doctorid) references doctor(doctorid) enable
);

CREATE TABLE sensor
(
	sensorid int NOT NULL ENABLE,
    sensornum int,
    type_of_sensor VARCHAR2(45 byte),
    careteamid int not null enable,
    patientid int not null enable,
    systemid int not null enable,
    CONSTRAINT CARETEAMFK FOREIGN KEY (careteamid) REFERENCES careteam(careteamid) enable,
    CONSTRAINT PATIENTFK FOREIGN KEY (patientid) REFERENCES patient(patientid) enable,
	CONSTRAINT SYSTEMFK FOREIGN KEY (systemid) REFERENCES system(systemid) enable,
    servicecod VARCHAR2(45 byte),
    servicedesc VARCHAR2(100 byte),
    admdate DATE,
    bed int,
    bodytemp int,
    bloodpress_systolic int,
    bloodpress_diastolic int,
    bpm int,
    sato2 int,
    timest timestamp, 
    CONSTRAINT SENSORID_PK PRIMARY KEY (sensorid)
);
