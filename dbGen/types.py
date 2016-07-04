class DataTypes:
    def __init__(self):
        return

    def __repr__(self):
        return str(self.__class__)

    def __str__(self):
        return self.__repr__()


class DataIntType(DataTypes):
    def __init__(self, lower, upper):
        DataTypes.__init__(self)
        self.lower = lower
        self.upper = upper


class DataListIntType(DataTypes):
    def __init__(self, lower):
        DataTypes.__init__(self)
        self.lower = lower


class DataRealType(DataTypes):
    def __init__(self, lower, upper, decimals):
        DataTypes.__init__(self)
        self.lower = lower
        self.upper = upper
        self.decimals = decimals


class DataStringType(DataTypes):
    def __init__(self):
        DataTypes.__init__(self)
