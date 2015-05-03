from bitstring import BitArray
import random

def onemax(bs):
        return bs.count(1)

def leadingones(bs):
        count = 0
        for c in bs:
                if (c != 1):
                        break
                count += 1
        return count

def jumpk(bs, k = 3):
        n = len(bs)
        if (onemax(bs) < (n-k)):
                return onemax(bs)
        elif ((n-k) <= onemax(bs)) and (onemax(bs) < n):
                return n - k
        elif (onemax(bs) == n):
                return n
        else:
                raise "WAT"

def royalroads(bs, k = 5):
        if (len(bs) % k != 0):
                raise ValueError("Not defined if n not divisible by k.")
        splits = [bs[x:x+k] for x in range(0, len(bs), k)]
        count = 0
        for split in splits:
                if set(split) == {1}:
                        count += 1
        return count

def binval(bs):
        return bs.uint

class FunctionObject:
        def __init__(self, function, optimum):
                self.function = function
                self.optimum = optimum
        def stopping_criterion_met(self, x):
                return (self.function(x) == self.optimum)
        def name(self):
                return self.function.__name__


def randombitstring(n):
        result = BitArray(float=random.random(), length=64)
        while (len(result) < n):
            temp = BitArray(float=random.random(), length=64)
            result.append(temp)
        return result[:n]


def rls(fo, n):
        x = randombitstring(n)
        iterations = 0
        while not (fo.stopping_criterion_met(x)):
                iterations += 1
                y = x.copy()
                i = random.randint(0, len(y) - 1)
                y.invert(i)
                if (fo.function(y) >= fo.function(x)):
                        x = y
        return iterations


def ea(fo, n):
        x = randombitstring(n)
        iterations = 0
        while not (fo.stopping_criterion_met(x)):
                iterations += 1
                y = x.copy()
                for i in range(0, len(y)):
                        if (random.random() < 0.1):
                                y.invert(i)
                if (fo.function(y) >= fo.function(x)):
                        x = y
        return iterations

def rls_modified(fo, n):
        x = randombitstring(n)
        iterations = 0
        while not (fo.stopping_criterion_met(x)):
                iterations += 1
                y = x.copy()
                i = random.randint(0, len(y) - 1)
                y.invert(i)
                if (fo.function(y) > fo.function(x)):
                        x = y
        return iterations


def ea_modified(fo, n):
        x = randombitstring(n)
        iterations = 0
        while not (fo.stopping_criterion_met(x)):
                iterations += 1
                y = x.copy()
                for i in range(0, len(y)):
                        if (random.random() < 0.1):
                                y.invert(i)
                if (fo.function(y) > fo.function(x)):
                        x = y
        return iterations


if __name__ == "__main__":
    input = randombitstring(25)
    n = len(input)
    fo_onemax = FunctionObject(onemax, n)
    fo_leadingones = FunctionObject(leadingones, n)
    fo_jumpk = FunctionObject(jumpk, n)
    fo_royalroads = FunctionObject(royalroads, n/5)
    fo_binval = FunctionObject(binval, 2**n - 1)
    for a in [rls, ea, rls_modified, ea_modified]:
            for f in [fo_onemax, fo_leadingones, fo_jumpk, fo_binval, fo_royalroads]:
                iterations = 0
                for t in range(0, 10):
                    iterations =+ a(f, n)
                average = iterations/10
                print(a.__name__, "and function", f.name(), "with n =", n,"  : ", average)

