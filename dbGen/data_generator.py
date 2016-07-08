def generate(table, count=100):
    """
    Generates the random data for a table
    :param table: The table to generate the random data for
    :param count: The number of data in the table
    :return: The result set that can be appended to the table
    """
    # name, data_type, key=False, reference=None, rows=None
    columns = table.column_map.values()
    types = [x.data_type for x in columns]
    keys = [x.key for x in columns]
    references = [x.reference for x in columns]
    results = []
    result = []
    for row in range(0, count):
        result.clear()
        for column in range(len(columns)):
            data_type = types[column]
            result.append(next(data_type))
        results.append(tuple(result))
    return results
