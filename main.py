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
            self._bird_count = sum(1 for line in open(self._bird_file, 'r'))
            self._n = 1

        def __next__(self):
            """
            Generates the next bird for the data type
            :return: The name of a bird
            """
            val = linecache.getline(self._bird_file, self._n).strip()
            self._n += 1
            return val

    # Create the birds table, this will have 29 members in it
    birds = g.Table("birds", 251)
    b1 = g.Column("bird_id", t.DataListIntType())
    b2 = g.Column("bird_name", BirdType())
    birds.add_column(b1)
    birds.add_column(b2)

    # Initialise the people table, it will have 7 members
    people = g.Table("people", 43)
    p1 = g.Column("person_id", t.DataListIntType())
    p2 = g.Column("person_name", t.DataNameType())
    people.add_column(p1)
    people.add_column(p2)

    # Initialise the sightings table, it will have 100 members
    sightings = g.Table("sightings", 5132)
    # A column that is a reference to another does not need a data type
    s1 = g.Column("person_id", None, people, people.column_map["person_id"], True)
    s2 = g.Column("bird_id", None, birds, birds.column_map["bird_id"], True)
    s3 = g.Column("latitude", t.DataRealType(-31, -25.2, 2))
    s4 = g.Column("longitude", t.DataRealType(150, 152.5, 2))
    # We use unix time here
    s5 = g.Column("epoch_time", t.DataIntType(1451606400, 1467331200))
    sightings.add_column(g.Column("sighting_id", t.DataListIntType()))
    sightings.add_column(s1)
    sightings.add_column(s2)
    sightings.add_column(s3)
    sightings.add_column(s4)
    sightings.add_column(s5)

    # Create the database schema object
    schema = g.Schema([birds, people, sightings])

    # Create the data
    dg.create(schema)
    for table in schema:
        print(table.get_sql_insert_statements())

if __name__ == '__main__':
    main()
