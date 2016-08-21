from dbGen import graph as g
from dbGen import data_generator as dg
from dbGen import database_types as t
import os
import linecache


def main():

    class BirdType(t.DataTypes):
        """
        A simple data type for bird names
        All custom data types inherit from database_types.DataTypes, note that database_types is aliased to t in this case
        It needs an __init__ and __next__ method to work with the generator
        """
        def __init__(self):
            """
            Initialises the bird class and instantiates any properties needed
            """
            t.DataTypes.__init__(self)
            # Since this is a string it needs to be surrounds by single quotation marks
            # If this is not filled then the default is to not surround it by anything
            self.opener = "'"
            self.closer = "'"
            self._bird_file = os.path.join('words', 'birds.txt')
            self._n = 1

        def __next__(self):
            """
            Generates the next bird for the data type
            :return: The name of a bird
            """
            val = linecache.getline(self._bird_file, self._n).strip()
            self._n += 1
            return val

    class CompanyNamesType(t.DataTypes):

        def __init__(self):
            t.DataTypes.__init__(self)
            self.opener = "'"
            self.closer = "'"
            self.database_type = "VARCHAR2(70)"
            self._company_file = os.path.join('words', 'companies.txt')
            self._n = 1

        def __next__(self):
            val = linecache.getline(self._company_file, self._n).strip()
            self._n += 1
            return val

    # Create the birds table, this will have 4472 members in it
    birds = g.Table("birds", 4472)
    b1 = g.Column("bird_id", t.DataListIntType(), primary_key=True)
    b2 = g.Column("bird_name", BirdType())
    birds.add_column(b1)
    birds.add_column(b2)

    # Initialise the organisations table, it will have 8 members
    organisations = g.Table("organisations", 8)
    c1 = g.Column("company_id", t.DataListIntType(), primary_key=True)
    c2 = g.Column("company_name", CompanyNamesType())
    organisations.add_column(c1)
    organisations.add_column(c2)

    # Initialise the people table, it will have 5132 members
    people = g.Table("people", 5132)
    p1 = g.Column("person_id", t.DataListIntType(), primary_key=True)
    p2 = g.Column("person_name", t.DataNameType())
    p3 = g.Column("date_of_birth", t.DataDateType('1970-01-02', '1995-12-31'))
    p4 = g.Column("company_id", None, organisations, organisations.column_map["company_id"], True)
    people.add_column(p1)
    people.add_column(p2)
    people.add_column(p3)
    people.add_column(p4)

    # Initialise the sightings table, it will have 267941 members
    sightings = g.Table("sightings", 267941)
    # A column that is a reference to another does not need a data type
    s1 = g.Column("sighting_id", t.DataListIntType(), primary_key=True)
    s2 = g.Column("person_id", None, people, people.column_map["person_id"], True)
    s3 = g.Column("bird_id", None, birds, birds.column_map["bird_id"], True)
    s4 = g.Column("latitude", t.DataRealType(-31, -25.2, 2))
    s5 = g.Column("longitude", t.DataRealType(150, 152.5, 2))
    s6 = g.Column("sighting_date", t.DataDateType('2000-01-01', '2016-01-02'))
    sightings.add_column(s1)
    sightings.add_column(s2)
    sightings.add_column(s3)
    sightings.add_column(s4)
    sightings.add_column(s5)
    sightings.add_column(s6)

    # Create the database schema object
    schema = g.Schema([birds, organisations, people, sightings])

    # Create the data
    dg.create(schema)

    for table in schema:
        print(table.get_create_table_statement(True))
    for table in schema:
        print(table.get_sql_insert_statements())

if __name__ == '__main__':
    main()
