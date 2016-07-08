from dbGen import graph as g
from dbGen import data_generator as dg
from dbGen import types as t
import os
import random

companies = g.Table("companies", [g.Column("id", t.DataListIntType(1), True), g.Column("name", t.DataNameType())])
print(companies.column_map)

movies = g.Table("movies")
c1 = g.Column("id", "integer", True)
c2 = g.Column("name", "String")

movies.add_column(c1)
movies.add_column(c2)

print(movies.has_references())

c3 = g.Column("company_id", "integer", False, companies.column_map["id"])
movies.add_column(c3)

print(movies.has_references())

schema = g.Schema([movies, companies])

print(schema)
print(schema.get_independent_tables())

companies.add_data(dg.generate(companies))
companies.print_data()

path = os.path.join(os.getcwd(), "nouns")

# int_type = t.DataRealType(0, 10)
# print(iter(int_type))
# print(next(int_type))
# print(next(int_type))
# print(next(int_type))
# print(next(int_type))
# print(next(int_type))
