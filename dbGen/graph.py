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

    def has_references(self):
        """
        Returns True if the table has a column that reference another table
        """
        return any(x for x in self._columns if x.reference is not None)

    def add_column(self, column):
        """
        Adds a column to the table
        """
        self._columns.append(column)
        self.column_map[column.name] = column

    def add_data(self, rows):
        """
        Adds given rows to the table

        Args:
            rows: a list in the form[(item1 ... itemN)]
        Return:
            True iff the operation succeeded otherwise False
        Will fail if the number of rows in the provided data != number of rows in the table
        """
        if len(rows) <= 0:
            # Well we did succeed at adding nothing
            return True
        if len(rows[0]) != len(self.column_map):
            return False
        for row in rows:
            for i, column in enumerate(row):
                self._columns[i].append(column)
        return True


class Column:
    def __init__(self, name, data_type, key=False, reference=None, rows=None):
        self.name = name
        self.data_type = data_type
        self.key = key
        self.reference = reference
        self.rows = list(rows) if rows is not None else []

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


class Row:
    def __init__(self, data):
        self.data = list(data)
