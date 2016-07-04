from dbGen import graph as g

companies = g.Table("companies", [g.Column("id", "integer", True), g.Column("name", "String")])
print(companies.column_map)

movies = g.Table("Movies")
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
