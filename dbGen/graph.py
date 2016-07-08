from collections import OrderedDict


class Schema:
    def __init__(self, tables=None):
        self.tables = list(tables) if tables is not None else []

    def __repr__(self):
        return str(self.tables)

    def __str__(self):
        return self.__repr__()

    def get_independent_tables(self):
        """
        Gets all tables that do not reference any other table
        :return: A list of tables in the schema that do not reference another table
        """
        return [x for x in self.tables if x.has_references() == False]


class Table:
    def __init__(self, table_name, columns=None):
        self.tableName = table_name
        self._columns = list(columns) if columns is not None else []
        self.column_map = OrderedDict((a.name, a) for a in self._columns)

    def __repr__(self):
        return self.tableName + " table"

    def __str__(self):
        return self.__repr__()

    def column_count(self):
        return len(self.column_map)

    def print_data(self):
        """
        Prints the data stored in the table
        :return: None
        """
        if self.column_count() <= 0:
            print("[]")
        result = ""
        for i in range(0, len(self._columns[0].data)):
            data = ""
            for column in self._columns:
                data += str(column.data[i]) + " "
            result += data.strip() + " "
        print(result.strip())

    def has_references(self):
        """
        Finds if this table references another table
        :return: True iff the the table references another table otherwise False
        """
        return any(x for x in self._columns if x.reference is not None)

    def add_column(self, column):
        """
        Adds a column to the table
        :param column: the column to be added
        :return: None
        """
        self._columns.append(column)
        self.column_map[column.name] = column

    def add_data(self, rows):
        """
        Adds given rows to the table
        Will fail if the number of rows in the provided data != number of rows in the table
        :param rows: a list in the form[(item1 ... itemN)]
        :return: True iff the operation succeeded otherwise False
        """
        if len(rows) <= 0:
            # Well we did succeed at adding nothing
            return True
        if len(rows[0]) != len(self.column_map):
            return False
        for row in rows:
            for i, column in enumerate(row):
                self._columns[i].data.append(column)
        return True


class Column:
    def __init__(self, name, data_type, key=False, reference=None):
        self.name = name
        self.data_type = data_type
        self.key = key
        self.reference = reference
        self.data = []

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.name == other.name \
                   and self.data_type == other.data_type \
                   and self.key == other.key \
                   and self.reference == other.reference
        elif isinstance(other, ''.__class__):
            return self.name == other
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return self.name \
               + " is of type " + str(self.data_type) \
               + ". Key status: " + str(self.key) \
               + ". References: " + str(self.reference)

    def __str__(self):
        return self.__str__()
