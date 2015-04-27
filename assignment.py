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

bitstring = '1100010101011001011110'

print("OneMax: ", onemax(bitstring))
print("LeadingOnes: ", leadingones(bitstring))
print("Jump K: ", jumpk(bitstring, 4))
print("BinVal: ", binval(bitstring))
