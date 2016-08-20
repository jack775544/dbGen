import random
import os
import linecache
import datetime


class DataTypes:
    def __init__(self):
        self.opener = ""
        self.closer = ""
        return

    def __repr__(self):
        return str(self.__class__)

    def __str__(self):
        return self.__repr__()

    def __iter__(self):
        return self

    def __next__(self):
        return str(1)


class DataIntType(DataTypes):
    """
    A data type that will generate random integers between lower and upper - 1
    """
    def __init__(self, lower, upper):
        DataTypes.__init__(self)
        self.lower = lower
        self.upper = upper

    def __next__(self):
        return random.randint(self.lower, self.upper-1)


class DataListIntType(DataTypes):
    """
    A data type that will generate a sequential list of numbers. This is most commonly used for primary keys
    """
    def __init__(self, lower=1, step=1):
        DataTypes.__init__(self)
        self.lower = lower
        self._step = step
        self._n = lower

    def __next__(self):
        n = self._n
        self._n += self._step
        return n


class DataRealType(DataTypes):
    """
    A data type that will generate a random real number between upper and lower with a set precision
    """
    def __init__(self, lower, upper, precision=2):
        DataTypes.__init__(self)
        self.lower = lower
        self.upper = upper
        self.decimals = precision

    def __next__(self):
        return "{0:.2f}".format(random.uniform(self.lower, self.upper))


class DataNameType(DataTypes):
    def __init__(self, names=2):
        """
        A data type class for generating names
        :param names: 0 if first name only, 1 if last name only, 2 for first and last name, otherwise undefined
        behaviour
        """
        DataTypes.__init__(self)
        self.opener = "'"
        self.closer = "'"
        self._names = names
        self._male_file = os.path.join('dbGen', 'nouns', 'malefirst.txt')
        self._female_file = os.path.join('dbGen', 'nouns', 'femalefirst.txt')
        self._last_file = os.path.join('dbGen', 'nouns', 'lastname.txt')        
        self._male_count = sum(1 for line in open(self._male_file, 'r'))
        self._female_count = sum(1 for line in open(self._female_file, 'r'))
        self._last_count = sum(1 for line in open(self._last_file, 'r'))

    def __next__(self):
        gender_file, gender_count = (self._male_file, self._male_count) if random.random() < 0.5 \
            else (self._female_file, self._female_count)
        if self._names == 0:
            return linecache.getline(gender_file, random.randint(1, gender_count)).strip().title()
        elif self._names == 1:
            return linecache.getline(self._last_file, random.randint(1, self._last_count)).strip().title()
        elif self._names == 2:
            return linecache.getline(gender_file, random.randint(1, gender_count)).strip().title() + \
                " " + linecache.getline(self._last_file, random.randint(1, self._last_count)).strip().title()


class DataDateType(DataTypes):
    def __init__(self, start, end):
        """
        A data type class for generating dates

        :param start: A string representing the starting date
        :param end: A string representing the ending date, this must be greater than start

        The date format for this function is DD-MM-YYYY where all values are integers.
        For example, for the 19 January 2012 the format will be '19-01-2012'
        """
        DataTypes.__init__(self)
        self.opener = "'"
        self.closer = "'"
        self._month_file = os.path.join('dbGen', 'nouns', 'months.txt')
        self._start_year, self._start_month, self._start_day = map(int, start.split('-'))
        self._end_year, self._end_month, self._end_day = map(int, end.split('-'))
        self._start_stamp = int(datetime.datetime(self._start_year, self._start_month, self._start_day, 0, 0).timestamp())
        self._end_stamp = int(datetime.datetime(self._end_year, self._end_month, self._end_day, 23, 59).timestamp())

    def __next__(self):
        date = datetime.datetime.fromtimestamp(random.randint(self._start_stamp, self._end_stamp))
        return str(date.day) + '-' + linecache.getline(self._month_file, date.month).strip() + '-' + str(date.year)
