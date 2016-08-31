import random
from collections import OrderedDict


def create(schema):
    """
    Creates the data for a database schema
    :param schema: 
    :return:
    """
    data = schema.get_candidate_tables()
    temp = []
    while len(data):
        # Pop a table off the list and generate the data for it. Then regenerate the list
        table = data.pop()
        table.add_data(generate(table))
        schema.tables.remove(table)
        temp.append(table)
        data = schema.get_candidate_tables()
    temp.extend(schema.tables)
    schema.tables = temp


def generate(table):
    """
    Generates the random data for a table
    :param table: The table to generate the random data for
    :return: The result set that can be appended to the table
    """
    columns = table._columns
    types = [x.data_type for x in columns]
    results = []
    result = OrderedDict()
    count = table.length
    for row_num in range(0, count):
        for i in range(len(columns)):
            if columns[i].reference_column:
                if columns[i].rand_val is False:
                    result[columns[i].name] = (columns[i].reference_column.data[row_num % len(columns[i].reference_column.data)])
                else:
                    result[columns[i].name] = (columns[i].reference_column.data[random.randint(0, len(columns[i].reference_column.data) - 1)])
                continue
            data_type = types[i]
            result[columns[i].name] = get_next_value(data_type, result)
        results.append(tuple(result.values()))
        result = OrderedDict()
    return results


def get_next_value(data_type, values):
    if data_type.next_function.__name__ == '__next__':
        return data_type.next_function()
    else:
        return data_type.next_function(values)
