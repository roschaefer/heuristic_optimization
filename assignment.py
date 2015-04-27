def onemax(bs):
        return bs.count('1')

def leadingones(bs):
        count = 0
        for c in bs:
                if (c != '1'):
                        break
                count += 1
        return count

def jumpk(bs, k):
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
        return int(bs, 2)


def royalroads(bs, k):
        if (len(bs) % k != 0):
                raise ValueError("Not defined if n not divisible by k.")
        splits = [bs[x:x+k] for x in range(0, len(bs), k)]
        count = 0
        for split in splits:
                if set(split) == {'1'}:
                        count += 1
        return count


bitstring = '1111111101011001011110'

print("OneMax: ", onemax(bitstring))
print("LeadingOnes: ", leadingones(bitstring))
print("Jump K: ", jumpk(bitstring, 3))
print("BinVal: ", binval(bitstring))
print("RoyalRoads: ", royalroads(bitstring, 2))
