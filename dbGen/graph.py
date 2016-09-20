from collections import OrderedDict
from dbGen import database_types as t


class Schema:
    def __init__(self, tables=None):
        self.tables = list(tables) if tables is not None else []

    def __repr__(self):
        return str(self.tables)

    def __str__(self):
        return self.__repr__()

    def __iter__(self):
        return iter(self.tables)

    def __len__(self):
        return len(self.tables)

    def get_independent_tables(self):
        """
        Gets all tables that do not reference any other table
        :return: A list of tables in the schema that do not reference another table
        """
        return [x for x in self.tables if x.has_references() is False]

    def get_candidate_tables(self):
        results = []
        for table in self.tables:
            if table.has_references() is False and table.has_data is False:
                results.append(table)
                continue
            if table.has_references() and table.has_data is not True:
                references = table.get_referenced_tables()
                candidate = all(x.has_data for x in references)
                if candidate:
                    results.append(table)
                continue
        return results


class Table:
    def __init__(self, table_name, length=100, columns=None):
        self.table_name = table_name
        self._columns = list(columns) if columns is not None else []
        self.column_map = OrderedDict((a.name, a) for a in self._columns)
        self.has_data = False
        self.length = length

    def __repr__(self):
        return self.table_name + " table"

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
            return
        result = ""
        for i in range(0, len(self._columns[0].data)):
            data = ""
            for column in self._columns:
                data += str(column.data[i]) + " "
            result += data.strip() + ", "
        print(result.strip(", ") if result.strip() != "" else "Empty Table")

    def get_csv(self, lazy=True):
        """
        Gets a csv representation of each row in the table
        :param lazy: If True generates a lazy generator, otherwise it will generate a list
        :return: A list of comma separated values, with each item in the list representing a row in the table
        """
        if self.column_count() <= 0:
            return []
        result = []
        if lazy:
            return (', '.join([column.data_type.opener +
                               str(column.data[i]).replace("'", "") +
                               column.data_type.closer for column in self._columns]).strip(", ")
                    for i in range(0, self.length))
        for i in range(0, len(self._columns[0].data)):
            data = ""
            for column in self._columns:
                data += column.data_type.opener + str(column.data[i]).replace("'", "") + column.data_type.closer + ", "
            result.append(data.strip(", "))
        return result

    def get_sql_insert_statements(self, lazy=True):
        if lazy:
            return ("INSERT INTO " + self.table_name + " VALUES (" + line + ");\n" for line in self.get_csv())
        statements = ""
        for line in self.get_csv():
            statements += "INSERT INTO " + self.table_name + " VALUES (" + line + ");\n"
        return statements.strip()

    def get_create_table_statement(self, reference_statements=False):
        references = []
        keys = []
        uniques = []
        not_nulls = []
        statement = "CREATE TABLE " + self.table_name + "(\n"
        for column in self._columns:
            statement += "    " + column.name + " " + column.data_type.database_type + ",\n"
            if column.reference_table is not None:
                references.append(column)
            if column.primary_key is not False:
                keys.append(column)
            if column.unique is not False:
                uniques.append(column)
            if column.not_null is not False:
                not_nulls.append(column)
        statement = statement.strip(",\n")
        statement += "\n);\n"
        if reference_statements is not False:
            for column in keys:
                statement += "ALTER TABLE " + self.table_name + "\n"
                statement += "ADD CONSTRAINT PK_" + column.name + "\n"
                statement += "PRIMARY KEY (" + column.name + ");\n"
            for column in uniques:
                statement += "ALTER TABLE " + self.table_name + "\n"
                statement += "ADD CONSTRAINT UN_" + column.name + "\n"
                statement += "UNIQUE (" + column.name + ");\n"
            for column in not_nulls:
                statement += "ALTER TABLE " + self.table_name + "\n"
                statement += "ADD CONSTRAINT NN_" + column.name + "\n"
                statement += "CHECK (" + column.name + " IS NOT NULL);\n"
            for column in references:
                statement += "ALTER TABLE " + self.table_name + "\n"
                statement += "ADD CONSTRAINT FK_" + column.name + "_TO_" + column.reference_column.name + "\n"
                statement += "FOREIGN KEY (" + column.name + ") REFERENCES " + column.reference_table.table_name + " (" + column.reference_column.name + ");\n"
        return statement

    def has_references(self):
        """
        Finds if this table references another table
        :return: True iff the the table references another table otherwise False
        """
        return any(x for x in self._columns if x.reference_column is not None)

    def get_referenced_columns(self):
        results = []
        for column in self._columns:
            if column.reference_column is not None:
                results.append(column.reference_column)
        return results

    def get_referenced_tables(self):
        results = []
        for column in self._columns:
            if column.reference_table is not None:
                results.append(column.reference_table)
        return results

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
        self.has_data = True
        return True


class Column:
    def __init__(self, name, data_type, reference_table=None, reference_column=None, rand_val=False, primary_key=False, unique=False, not_null=False):
        self.name = name
        if reference_column is not None:
            self.data_type = reference_column.data_type
        elif data_type is not None:
            self.data_type = data_type
        else:
            self.data_type = t.DataTypes()
        self.reference_column = reference_column
        self.reference_table = reference_table
        self.data = []
        self.rand_val = rand_val
        self.primary_key = primary_key
        self.unique = unique
        self.not_null = not_null

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.name == other.name \
                   and self.data_type == other.data_type \
                   and self.reference_column == other.reference_column
        elif isinstance(other, ''.__class__):
            return self.name == other
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return self.name \
               + " is of type " + str(self.data_type) \
               + ". References: " + str(self.reference_column)

    def __str__(self):
        return self.__repr__()
