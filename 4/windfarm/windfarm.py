#!/usr/bin/env python
import optunity
from IPython import embed
import subprocess
from random import randint

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

def in_F1(point):
    x,y = point
    return (0<=x<4000) and (0<=y<10000)

def in_F2(point):
    x,y = point
    return (6000<=x<10000) and (0<=y<10000)

def in_F3(point):
    x,y = point
    return (0<=x<10000) and (2000<=y<8000)

def bound_box_constraint(points):
    for p in points:
        if ( not (in_F1(p) or in_F2(p) or in_F3(p))):
                return False
        return True

def security_distance_constraint(points):
    for x1,y1 in points:
        for x2,y2 in points:
            if ((x1-x2)**2 + (y1-y2)**2) >= 308:
                return False
    return True

def good_points():
    pos = points()
    while not (bound_box_constraint(pos) and security_distance_constraint(pos)):
        pos = points()
    return pos

def costs():
    print_points(points())
    ps = subprocess.Popen(("cat", "optimized.dat"), stdout=subprocess.PIPE)
    costs = subprocess.check_output(("./fcost"), stdin=ps.stdout)
    return float(costs)

embed()
