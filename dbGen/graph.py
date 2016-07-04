class Schema:
    def __init__(self, tables=None):
        self.tables = list(tables) if tables is not None else []

    def __repr__(self):
        return str(self.tables)

    def __str__(self):
        return self.__repr__()

    '''
    Gets all tables that do not reference any other table
    '''
    def get_independent_tables(self):
        return [x for x in self.tables if x.has_references() == False]


class Table:
    def __init__(self, table_name, columns=None):
        self.tableName = table_name
        self._columns = list(columns) if columns is not None else []
        self.column_map = {a.name: a for a in self._columns}

    def __repr__(self):
        return self.tableName + " table"

    def __str__(self):
        return self.__repr__()

    '''
    Returns True if the table has a column that reference another table
    '''
    def has_references(self):
        return any(x for x in self._columns if x.reference is not None)

    '''
    Appends a column to the table
    '''
    def append(self, column):
        self._columns.append(column)
        self.column_map[column.name] = column


class Column:
    def __init__(self, name, data_type, key=False, reference=None):
        self.name = name
        self.dataType = data_type
        self.key = key
        self.reference = reference

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.name == other.name \
                   and self.dataType == other.dataType \
                   and self.key == other.key \
                   and self.reference == other.reference
        elif isinstance(other, ''.__class__):
            return self.name == other
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return self.name \
               + " is of type " + self.dataType \
               + ". Key status: " + str(self.key) \
               + ". References: " + str(self.reference)

    def __str__(self):
        return self.__str__()
