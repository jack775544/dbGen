from dbGen import graph as g
from dbGen import data_generator as dg
from dbGen import database_types as t
import os

companies = g.Table("companies", [g.Column("id", t.DataListIntType(1)), g.Column("name", t.DataNameType())])
print(companies.column_map)

movies = g.Table("movies")
c1 = g.Column("id", t.DataListIntType(10000))
c2 = g.Column("name", t.DataNameType())

movies.add_column(c1)
movies.add_column(c2)

print(movies.has_references())

c3 = g.Column("company_id", None, companies.column_map["id"])
movies.add_column(c3)

print(movies.has_references())

schema = g.Schema([movies, companies])

print(schema)
print(schema.get_independent_tables())

companies.add_data(dg.generate(companies))
companies.print_data()

movies.add_data(dg.generate(movies, 200))
movies.print_data()

path = os.path.join(os.getcwd(), "nouns")
print(path)

