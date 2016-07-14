import random
import os
import linecache


class DataTypes:
    def __init__(self):
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
    def __init__(self, lower, upper):
        DataTypes.__init__(self)
        self.lower = lower
        self.upper = upper

    def __next__(self):
        return random.randint(self.lower, self.upper-1)


class DataListIntType(DataTypes):
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
        self._names = names
        self._male_file = os.path.join('dbGen', 'nouns', 'malefirst.txt')
        self._female_file = os.path.join('dbGen', 'nouns', 'femalefirst.txt')
        self._last_file = os.path.join('dbGen', 'nouns', 'lastname.txt')        
        self._male_count = sum(1 for line in open(self._male_file, 'r'))
        self._female_count = sum(1 for line in open(self._female_file, 'r'))
        self._last_count = sum(1 for line in open(self._last_file, 'r'))

    def __next__(self):
        gender_file, gender_count = (self._male_file, self._male_count) if random.random() < 0.5 else (self._female_file, self._female_count)
        if self._names == 0:
            return linecache.getline(gender_file, random.randint(1, gender_count)).strip().title()
        elif self._names == 1:
            return linecache.getline(self._last_file, random.randint(1, self._last_count)).strip().title()
        elif self._names == 2:
            return linecache.getline(gender_file, random.randint(1, gender_count)).strip().title() + \
                " " + linecache.getline(self._last_file, random.randint(1, self._last_count)).strip().title()
