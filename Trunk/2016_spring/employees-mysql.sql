-- Employee Schema, MySQL Version
-- SQL:  Practical Guide for Developers
-- Michael J. Donahoo and Gregory D. Speegle
-- Copyright 2005

DROP DATABASE IF EXISTS employees;

CREATE DATABASE employees;

USE employees;

CREATE TABLE employees (
  employeeid NUMERIC(9) NOT NULL,
  firstname VARCHAR(10),
  lastname VARCHAR(20),
  deptcode CHAR(5),
  salary NUMERIC(9, 2),
  PRIMARY KEY(employeeid)
);

CREATE TABLE departments (
  code CHAR(5) NOT NULL,
  name VARCHAR(30),
  managerid NUMERIC(9),
  subdeptof CHAR(5),
  PRIMARY KEY(code),
  FOREIGN KEY(managerid) REFERENCES employees(employeeid),
  FOREIGN KEY(subdeptof) REFERENCES departments(code)
);

ALTER TABLE employees ADD FOREIGN KEY (deptcode) REFERENCES departments(code);

CREATE TABLE projects (
  projectid CHAR(8) NOT NULL,
  deptcode CHAR(5),
  description VARCHAR(200),
  startdate DATE,
  enddate DATE,
  revenue NUMERIC(12, 2),
  PRIMARY KEY(projectid),
  FOREIGN KEY(deptcode) REFERENCES departments(code)
);

CREATE TABLE workson (
  employeeid NUMERIC(9) NOT NULL,
  projectid CHAR(8) NOT NULL,
  assignedtime DECIMAL(3,2),
  PRIMARY KEY(employeeid, projectid),
  FOREIGN KEY(employeeid) REFERENCES employees(employeeid),
  FOREIGN KEY(projectid) REFERENCES projects(projectid)
);

INSERT INTO departments VALUES ('ADMIN', 'Administration', NULL, NULL);
INSERT INTO departments VALUES ('ACCNT', 'Accounting', NULL, 'ADMIN');
INSERT INTO departments VALUES ('CNSLT', 'Consulting', NULL, 'ADMIN');
INSERT INTO departments VALUES ('HDWRE', 'Hardware', NULL, 'CNSLT');

INSERT INTO employees VALUES (1, 'Al', 'Betheleader', 'ADMIN', 70000);
INSERT INTO employees VALUES (2, 'PI', 'Rsquared', 'ACCNT', 40000);
INSERT INTO employees VALUES (3, 'Harry', 'Hardware', 'HDWRE', 50000);
INSERT INTO employees VALUES (4, 'Sussie', 'Software', 'CNSLT', 60000);
INSERT INTO employees VALUES (5, 'Abe', 'Advice', 'CNSLT', 30000);
INSERT INTO employees VALUES (6, 'Hardly', 'Aware', NULL, 65000);

UPDATE departments SET managerid = 1 WHERE code = 'ADMIN';
UPDATE departments SET managerid = 2 WHERE code = 'ACCNT';
UPDATE departments SET managerid = 3 WHERE code = 'HDWRE';
UPDATE departments SET managerid = 4 WHERE code = 'CNSLT';

INSERT INTO projects VALUES ('EMPHAPPY', 'ADMIN', 'Employee Moral', '2002-03-14', NULL, 0);
INSERT INTO projects VALUES ('ROBOSPSE', 'CNSLT', 'Robotic Spouse', '2002-03-14', NULL, 200000);
INSERT INTO projects VALUES ('ADT4MFIA', 'ACCNT', 'Mofia Audit', '2003-07-3', '2003-11-30', 100000);
INSERT INTO PROJECTS VALUES ('DNLDCLNT', 'CNSLT', 'Download Client', '2005-02-03', NULL, 15000);

INSERT INTO workson VALUES (2, 'ADT4MFIA', 0.50);
INSERT INTO workson VALUES (3, 'ROBOSPSE', 0.75);
INSERT INTO workson VALUES (4, 'ROBOSPSE', 0.75);
INSERT INTO workson VALUES (5, 'ROBOSPSE', 0.50);
INSERT INTO workson VALUES (5, 'ADT4MFIA', 0.60);
INSERT INTO workson VALUES (3, 'DNLDCLNT', 0.25);


/////Stripped version


CREATE TABLE emp_employees (
  employeeid NUMERIC(9) NOT NULL,
  firstname VARCHAR(10),
  lastname VARCHAR(20),
  deptcode CHAR(5),
  salary NUMERIC(9, 2),
  PRIMARY KEY(employeeid)
);

CREATE TABLE emp_departments (
  code CHAR(5) NOT NULL,
  name VARCHAR(30),
  managerid NUMERIC(9),
  subdeptof CHAR(5),
  PRIMARY KEY(code),
);


CREATE TABLE emp_projects (
  projectid CHAR(8) NOT NULL,
  deptcode CHAR(5),
  description VARCHAR(200),
  startdate DATE,
  enddate DATE,
  revenue NUMERIC(12, 2),
  PRIMARY KEY(projectid),
);

CREATE TABLE emp_workson (
  employeeid NUMERIC(9) NOT NULL,
  projectid CHAR(8) NOT NULL,
  assignedtime DECIMAL(3,2),
  PRIMARY KEY(employeeid, projectid),
);

INSERT INTO emp_departments VALUES ('ADMIN', 'Administration', NULL, NULL);
INSERT INTO emp_departments VALUES ('ACCNT', 'Accounting', NULL, 'ADMIN');
INSERT INTO emp_departments VALUES ('CNSLT', 'Consulting', NULL, 'ADMIN');
INSERT INTO emp_departments VALUES ('HDWRE', 'Hardware', NULL, 'CNSLT');

INSERT INTO emp_employees VALUES (1, 'Al', 'Betheleader', 'ADMIN', 70000);
INSERT INTO emp_employees VALUES (2, 'PI', 'Rsquared', 'ACCNT', 40000);
INSERT INTO emp_employees VALUES (3, 'Harry', 'Hardware', 'HDWRE', 50000);
INSERT INTO emp_employees VALUES (4, 'Sussie', 'Software', 'CNSLT', 60000);
INSERT INTO emp_employees VALUES (5, 'Abe', 'Advice', 'CNSLT', 30000);
INSERT INTO emp_employees VALUES (6, 'Hardly', 'Aware', NULL, 65000);

UPDATE emp_departments SET managerid = 1 WHERE code = 'ADMIN';
UPDATE emp_departments SET managerid = 2 WHERE code = 'ACCNT';
UPDATE emp_departments SET managerid = 3 WHERE code = 'HDWRE';
UPDATE emp_departments SET managerid = 4 WHERE code = 'CNSLT';

INSERT INTO emp_projects VALUES ('EMPHAPPY', 'ADMIN', 'Employee Moral', '2002-03-14', NULL, 0);
INSERT INTO emp_projects VALUES ('ROBOSPSE', 'CNSLT', 'Robotic Spouse', '2002-03-14', NULL, 200000);
INSERT INTO emp_projects VALUES ('ADT4MFIA', 'ACCNT', 'Mofia Audit', '2003-07-3', '2003-11-30', 100000);
INSERT INTO emp_PROJECTS VALUES ('DNLDCLNT', 'CNSLT', 'Download Client', '2005-02-03', NULL, 15000);

INSERT INTO emp_workson VALUES (2, 'ADT4MFIA', 0.50);
INSERT INTO emp_workson VALUES (3, 'ROBOSPSE', 0.75);
INSERT INTO emp_workson VALUES (4, 'ROBOSPSE', 0.75);
INSERT INTO emp_workson VALUES (5, 'ROBOSPSE', 0.50);
INSERT INTO emp_workson VALUES (5, 'ADT4MFIA', 0.60);
INSERT INTO emp_workson VALUES (3, 'DNLDCLNT', 0.25);
