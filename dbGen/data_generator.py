from dbGen import types as t


def generate(table, count=100):
    """
    Generates random data for the table. If this table has a reference to another table in it then the other table is
    expected to already have data in it. This method will not work on tables that reference themselves
    """
    # name, data_type, key=False, reference=None, rows=None
    columns = table.column_map.values()
    types = [x.data_type for x in columns]
    keys = [x.key for x in columns]
    references = [x.reference for x in columns]
    results = []
    for i in range(0, count):
        result = []
        for j in range(len(columns)):
            if type(types[j]) == t.DataListIntType:
                result.append(i)
            else:
                result.append("hello")
        results.append(tuple(result))
    return results
