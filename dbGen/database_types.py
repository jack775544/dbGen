import random


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
        self.names = names

    def __next__(self):
        return "WORDS"
