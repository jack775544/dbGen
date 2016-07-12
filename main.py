from dbGen import graph as g
from dbGen import data_generator as dg
from dbGen import database_types as t
import os

companies = g.Table("companies", [g.Column("id", t.DataListIntType(1)), g.Column("name", t.DataNameType())])

movies = g.Table("movies")
c1 = g.Column("id", t.DataListIntType(10000))
c2 = g.Column("name", t.DataNameType())

movies.add_column(c1)
movies.add_column(c2)

c3 = g.Column("company_id", None, companies, companies.column_map["id"])
movies.add_column(c3)

schema = g.Schema([movies, companies])
schema.get_candidate_tables()

dg.create(schema)
for t in schema:
    t.print_data()
