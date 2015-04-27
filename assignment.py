def onemax(bitstring):
        return bitstring.count('1')

def leadingones(bitstring):
        count = 0
        for c in bitstring:
                if c != '1':
                        break
                count += 1
        return count


print(leadingones('111100011'))
