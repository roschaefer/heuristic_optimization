#!/usr/bin/env python
import optunity
from IPython import embed
import subprocess
from random import randint

#def f(x, y):
    #return -x**2 - y**2

#optimal_pars, details, _ = optunity.maximize(f, num_evals=100, x=[-5, 5], y=[-5, 5])

def points():
    return  [(randint(0,10000),randint(0,10000)) for _ in range(100)]

def points_formatted(points):
    return '\n'.join([' '.join(map(str,p)) for p in points])




def print_points(points):
    with open('optimized.dat', 'w') as the_file:
            the_file.write(str(len(points)))
            the_file.write('\n')
            the_file.write(points_formatted(points))
            the_file.write('\n')

print_points(points())

ps = subprocess.Popen(("cat", "optimized.dat"), stdout=subprocess.PIPE)
cost = subprocess.check_output(("./fcost"), stdin=ps.stdout)

embed()
