from dbGen import graph as g
from dbGen import data_generator as dg
from dbGen import types as t

companies = g.Table("companies", [g.Column("id", t.DataListIntType(1), True), g.Column("name", t.DataStringType())])
print(companies.column_map)

movies = g.Table("movies")
c1 = g.Column("id", "integer", True)
c2 = g.Column("name", "String")

movies.append(c1)
movies.append(c2)

print(movies.has_references())

c3 = g.Column("company_id", "integer", False, companies.column_map["id"])
movies.append(c3)

print(movies.has_references())

schema = g.Schema([movies, companies])

print(schema)
print(schema.get_independent_tables())

print(dg.generate(companies))
