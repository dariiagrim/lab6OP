from abc import ABC, abstractmethod
import math


class Function(ABC):
    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        if type(value) == float or type(value) == int:
            self.__x = value
        else:
            raise ValueError("Not supported type")

    @property
    def m(self):
        return self.__m

    @m.setter
    def m(self, value):
        if type(value) == int and value > 0:
            self.__m = value
        else:
            raise ValueError("Not supported type")

    @abstractmethod
    def calc(self):
        raise NotImplementedError


class SquareRoot(Function):
    def __init__(self, x):
        self.x = x

    @Function.x.setter
    def x(self, value):
        Function.x.fset(self, value)
        if value > 1 or value < -1:
            raise ValueError

    def calc(self):
        result = 0
        m = 0
        while True:
            s = (math.pow(-1, m)*math.factorial(2*m)*math.pow(self.x, m))/((1-2*m)*math.pow(math.factorial(m), 2)*math.pow(4, m))
            if abs(s) < 0.0001:
                break
            result += s
            m += 1

        return result


class Sequence(Function):
    def __init__(self, x, m):
        self.x = x
        self.m = m

    @Function.x.setter
    def x(self, value):
        Function.x.fset(self, value)
        if value == 1:
            raise ValueError

    def calc(self):
        result = 0
        for i in range(self.m + 1):
            result += math.pow(self.x, i)
        return result


root = SquareRoot(-0.5)
print(root.calc())

seq = Sequence(2, 1)
print(seq.calc())
