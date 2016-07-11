def generate(table, count=100):
    """
    Generates the random data for a table
    :param table: The table to generate the random data for
    :param count: The number of data in the table
    :return: The result set that can be appended to the table
    """
    # name, data_type, reference=None, rows=None
    columns = table._columns
    types = [x.data_type for x in columns]
    results = []
    result = []
    for row_num in range(0, count):
        for i in range(len(columns)):
            if columns[i].reference:
                result.append(columns[i].reference.data[row_num % len(columns[i].reference.data)])
                continue
            data_type = types[i]
            result.append(next(data_type))
        results.append(tuple(result))
        result = []
    return results
