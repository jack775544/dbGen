from dbGen import graph as g
from dbGen import data_generator as dg
from dbGen import database_types as t
import os
import linecache


class BirdType(t.DataTypes):
    def __init__(self):
        t.DataTypes.__init__(self)
        self._bird_file = os.path.join('words', 'birds.txt')
        self._bird_count = sum(1 for line in open(self._bird_file, 'r'))
        self._n = 1

    def __next__(self):
        val = linecache.getline(self._bird_file, self._n).strip()
        self._n += 1
        return val


birds = g.Table("birds", 29)
b1 = g.Column("bird_id", t.DataListIntType())
b2 = g.Column("bird_name", BirdType())
birds.add_column(b1)
birds.add_column(b2)

people = g.Table("people", 8)
p1 = g.Column("person_id", t.DataListIntType())
p2 = g.Column("person_name", t.DataNameType())
people.add_column(p1)
people.add_column(p2)

sightings = g.Table("sightings", 100)
s1 = g.Column("person_id", None, people, people.column_map["person_id"])
s2 = g.Column("bird_id", None, birds, birds.column_map["bird_id"])
s3 = g.Column("lat", t.DataRealType(-31, -25.2, 2))
s4 = g.Column("long", t.DataRealType(150, 152.5, 2))
sightings.add_column(s1)
sightings.add_column(s2)
sightings.add_column(s3)
sightings.add_column(s4)

schema = g.Schema([birds, people, sightings])

dg.create(schema)
for table in schema:
    table.print_data()
