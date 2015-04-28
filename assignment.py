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

def binval(bs):
        return bs.uint


def royalroads(bs, k = 5):
        if (len(bs) % k != 0):
                raise ValueError("Not defined if n not divisible by k.")
        splits = [bs[x:x+k] for x in range(0, len(bs), k)]
        count = 0
        for split in splits:
                if set(split) == {1}:
                        count += 1
        return count




def randombitstring(n):
        result = BitArray(float=random.random(), length=64)
        while (len(result) < n):
            temp = BitArray(float=random.random(), length=64)
            result.append(temp)
        return result[:n]


def error(function, x, original):
        return abs(function(x) - function(original))


def rls(function, original):
        x = randombitstring(len(original))
        iterations = 0
        while not (error(function, x, original) == 0):
                iterations += 1
                y = x.copy()
                i = random.randint(0, len(y) - 1)
                y.invert(i)
                if (error(function, y, original) <= error(function, x, original)):
                        x = y
        return iterations


def ea(function, original):
        x = randombitstring(len(original))
        iterations = 0
        while not (error(function, x, original) == 0):
                iterations += 1
                y = x.copy()
                for i in range(0, len(y)):
                        if (random.random() < 0.1):
                                y.invert(i)
                if (error(function, y, original) <= error(function, x, original)):
                        x = y
        return iterations

def rls_modified(function, original):
        x = randombitstring(len(original))
        iterations = 0
        while not (error(function, x, original) == 0):
                iterations += 1
                y = x.copy()
                i = random.randint(0, len(y) - 1)
                y.invert(i)
                if (error(function, y, original) < error(function, x, original)):
                        x = y
        return iterations


def ea_modified(function, original):
        x = randombitstring(len(original))
        iterations = 0
        while not (error(function, x, original) == 0):
                iterations += 1
                y = x.copy()
                for i in range(0, len(y)):
                        if (random.random() < 0.1):
                                y.invert(i)
                if (error(function, y, original) < error(function, x, original)):
                        x = y
        return iterations


if __name__ == "__main__":
    input = randombitstring(25)
    for a in [rls, ea, rls_modified, ea_modified]:
            for f in [onemax, leadingones, jumpk, binval]:
                n = 0
                for t in range(0, 10):
                    n =+ a(f, input)
                average = n/10
                print(a.__name__, "and function", f.__name__, "with n =", len(input),"  : ", average)

