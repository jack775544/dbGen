# dbGen
A random data generator made for relational databases

Installation
---
- Install Python 3.5 for your platform
- Clone the repository
- Done!

There are no dependencies in this project  and it has only been tested on Python 3.5 for Windows.

Usage
---
Run the following command

	python main.py > out.sql

Example
---
The example code is documented and shows off all the built in data types and how to make a new custom data type. The
test has the following schema:

	/* This is tested in Oracle XE 11g */

	CREATE TABLE birds (
        bird_id INTEGER PRIMARY KEY,
        bird_name VARCHAR2(50)
    );
    
    CREATE TABLE people (
        person_id INTEGER PRIMARY KEY,
        person_name VARCHAR2(30)
    );
    
    CREATE TABLE sightings (
    	sighting_id INTEGER,
        person_id INTEGER,
        bird_id INTEGER,
        latitude REAL,
        longitude REAL,
        epoch_time INTEGER,
        CONSTRAINT fk_person_id FOREIGN KEY (person_id) REFERENCES people(person_id),
        CONSTRAINT fk_bird_id FOREIGN KEY (bird_id) REFERENCES birds(bird_id)
    );

dbGen will create a set of insert statements that will fit this schema once the data schema layout has been inserted
into the program.