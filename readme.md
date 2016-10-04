# dbGen
A random data generator made for relational databases

## Installation
- Install Python 3.5 for your platform
- Clone the repository
- Done!

There are no dependencies in this project.

This has been tested mainly on Python 3.5 for Ubuntu.

On Windows this will work in Python 3.5 for generating small datasets, 
however will throw an error on larger ones for unknown reasons. 

## Usage
Run the following command

	python main.py > out.sql

## Example
main.py contains a fully worked example of how to create a new dataset using the built in and custom datatypes,
as well as a an example of using prior generated values.

dbGen will create a set of `CREATE TABLE`, `ADD CONSTRAINT` and `INSERT INTO` statements
that fit to the schema that you provide. 