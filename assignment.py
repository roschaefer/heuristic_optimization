import random
import matplotlib.pyplot as plt

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
                if all((x == 1) for x in split):
                        count += 1
        return count

def binval(bs):
        return int("".join(str(x) for x in bs), 2)

class FunctionObject:
        def __init__(self, function, optimum):
                self.function = function
                self.optimum = optimum
        def stopping_criterion_met(self, x):
                return (self.function(x) == self.optimum)
        def name(self):
                return self.function.__name__


def randombitstring(n):
        bs = []
        for i in range(n):
                if (random.random() < .5):
                        bs.append(1)
                else:
                        bs.append(0)
        return bs


def rls(fo, n):
        x = randombitstring(n)
        iterations = 0
        while not (fo.stopping_criterion_met(x)):
                iterations += 1
                y = x.copy()
                i = random.randint(0, n - 1)
                y[i] = 1 - y[i]
                if (fo.function(y) >= fo.function(x)):
                        x = y
        return iterations


def ea(fo, n):
        x = randombitstring(n)
        iterations = 0
        while not (fo.stopping_criterion_met(x)):
                iterations += 1
                y = x.copy()
                for i in range(0, n):
                        if (random.random() < .1):
                                y[i] = 1 - y[i]
                if (fo.function(y) >= fo.function(x)):
                        x = y
        return iterations

def rls_modified(fo, n):
        x = randombitstring(n)
        iterations = 0
        while not (fo.stopping_criterion_met(x)):
                iterations += 1
                y = x.copy()
                i = random.randint(0, n - 1)
                y[i] = 1 - y[i]
                if (fo.function(y) > fo.function(x)):
                        x = y
        return iterations


def ea_modified(fo, n):
        x = randombitstring(n)
        iterations = 0
        while not (fo.stopping_criterion_met(x)):
                iterations += 1
                y = x.copy()
                for i in range(0, n):
                        if (random.random() < .1):
                                y[i] = 1 - y[i]
                if (fo.function(y) > fo.function(x)):
                        x = y
        return iterations

def plot(plotted_function, plotinput, labels):
        plt.xlabel("n")
        plt.ylabel("iterations")
        plt.title("Comparison of RLS and EA for f={function}".format(function=plotted_function.__name__))
        lineObjects = plt.plot(*plotinput)
        plt.legend(iter(lineObjects), labels)
        plt.savefig("plot_{function}.png".format(function=plotted_function.__name__))
        plt.close()

if __name__ == "__main__":
        step = 25


        # PLOT onemax (all)
        n_steps = 3
        n_range = range(step, step*n_steps +1, step)
        t = []
        for n in n_range:
            t.append(n)

        plotted_function = onemax
        plotinput = []
        labels = []
        for a in [rls, ea, rls_modified, ea_modified]:
                averages = []
                labels.append(a.__name__)
                for n in n_range:
                        fo = FunctionObject(plotted_function, n)
                        iterations = 0
                        for times in range(0, 10):
                            iterations += a(fo, n)
                        averages.append(iterations/10)
                plotinput.append(t)
                plotinput.append(averages)
                plotinput.append('s-')
        plot(plotted_function, plotinput, labels)




        # PLOT leadingones(all)
        n_steps = 3
        n_range = range(step, step*n_steps +1, step)
        t = []
        for n in n_range:
            t.append(n)

        plotted_function = leadingones
        plotinput = []
        labels = []
        for a in [rls, ea, rls_modified, ea_modified]:
                averages = []
                labels.append(a.__name__)
                for n in n_range:
                        fo = FunctionObject(plotted_function, n)
                        iterations = 0
                        for times in range(0, 10):
                            iterations += a(fo, n)
                        averages.append(iterations/10)
                plotinput.append(t)
                plotinput.append(averages)
                plotinput.append('s-')
        plot(plotted_function, plotinput, labels)

        # PLOT jumpk(rls, ea)
        n_steps = 2
        n_range = range(step, step*n_steps +1, step)
        t = []
        for n in n_range:
            t.append(n)

        plotted_function = jumpk
        plotinput = []
        labels = []
        for a in [rls, ea]:
                averages = []
                labels.append(a.__name__)
                for n in n_range:
                        fo = FunctionObject(plotted_function, n)
                        iterations = 0
                        for times in range(0, 10):
                            iterations += a(fo, n)
                        averages.append(iterations/10)
                plotinput.append(t)
                plotinput.append(averages)
                plotinput.append('s-')
        plot(plotted_function, plotinput, labels)

        # PLOT royalroads(rls, ea)
        n_steps = 3
        n_range = range(step, step*n_steps +1, step)
        t = []
        for n in n_range:
            t.append(n)

        plotted_function = royalroads
        plotinput = []
        labels = []
        for a in [rls, ea]:
                averages = []
                labels.append(a.__name__)
                for n in n_range:
                        fo = FunctionObject(plotted_function, n/5)
                        iterations = 0
                        for times in range(0, 10):
                            iterations += a(fo, n)
                        averages.append(iterations/10)
                plotinput.append(t)
                plotinput.append(averages)
                plotinput.append('s-')
        plot(plotted_function, plotinput, labels)


        # PLOT binval(all)
        n_steps = 3
        n_range = range(step, step*n_steps +1, step)
        t = []
        for n in n_range:
            t.append(n)

        plotted_function = binval
        plotinput = []
        labels = []
        for a in [rls, ea, rls_modified, ea_modified]:
                averages = []
                labels.append(a.__name__)
                for n in n_range:
                        fo = FunctionObject(plotted_function, 2**n -1)
                        iterations = 0
                        for times in range(0, 10):
                            iterations += a(fo, n)
                        averages.append(iterations/10)
                plotinput.append(t)
                plotinput.append(averages)
                plotinput.append('s-')
        plot(plotted_function, plotinput, labels)


