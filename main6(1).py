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
            if abs(s) < 0.000000001:
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


def work():
    r = "sqrt(1+x)"
    s = "(1-x^(m+1))/(1-x)"
    print(f"Hrymalska Dariia, Var 6, Level B, calculate {r} and {s}")

    while True:
        is_root = bool(int(input("If you want to calculate square root: enter 1, otherwise: enter 0 - ")))
        if is_root:
            x = float(input("Enter x(|x|<=1): "))
            try:
                root: Function = SquareRoot(x)
            except ValueError:
                print("Unsupported value, try again")
                continue
            print("Result: ", root.calc())
            end = input("Do you want to exit?(+/-)")
            if end == "+":
                break
        else:
            x = float(input("Enter x(!=1): "))
            m = int(input("Enter m(Natural): "))
            try:
                seq: Function = Sequence(x, m)
            except ValueError:
                print("Unsupported value, try again")
                continue
            print("Result", seq.calc())
            end = input("Do you want to exit?(+/-)")
            if end == "+":
                break


work()


