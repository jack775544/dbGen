from dbGen import graph


def create(schema):
    data = schema.get_candidate_tables()
    while len(data):
        table = data.pop()
        table.add_data(generate(table))
        data = schema.get_candidate_tables()


def generate(table):
    """
    Generates the random data for a table
    :param table: The table to generate the random data for
    :return: The result set that can be appended to the table
    """
    # name, data_type, reference=None, rows=None
    columns = table._columns
    types = [x.data_type for x in columns]
    results = []
    result = []
    count = table.length
    for row_num in range(0, count):
        for i in range(len(columns)):
            if columns[i].reference_column:
                result.append(columns[i].reference_column.data[row_num % len(columns[i].reference_column.data)])
                continue
            data_type = types[i]
            result.append(next(data_type))
        results.append(tuple(result))
        result = []
    return results
