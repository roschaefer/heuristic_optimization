#!/usr/bin/env python
# import optunity
import math
import operator
# from IPython import embed
import subprocess
from random import randint
import random
import matplotlib.pyplot as plt

def points_formatted(points):
    return '\n'.join([' '.join(map(str,p)) for p in points])

def print_optimized(points, costs):
    with open('optimized.dat', 'w') as the_file:
            the_file.write(str(len(points)))
            the_file.write('\n')
            the_file.write(points_formatted(points))
            the_file.write('\n')
    with open('optimized.val', 'w') as the_file:
            the_file.write(costs)

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
    for i in range(len(points)):
        x1, y1 = points[i]
        for x2,y2 in points[i+1:]:
            if (math.sqrt((x1-x2)**2 + (y1-y2)**2)) < 308:
                return False
    return True

def complies_constraints(points):
    return bound_box_constraint(points) and security_distance_constraint(points)


def costs(points):
    ps = subprocess.Popen(("cat", "optimized.dat"), stdout=subprocess.PIPE)
    costs = subprocess.check_output(("./fcost"), stdin=ps.stdout)
    return float(costs)

def read_points():
    with open ("initial.dat", "r") as myfile:
        data=myfile.readlines()
    points = list()
    for line in data[1:]:
        points.append(tuple(map(int, line.split())))
    return points

def modify(points, sigma):
    points = list(points) # same as copy() but compatible with python 2.7
    moveThese = random.getrandbits(len(points))
    for i in range(len(points)):
        if random.randint(0, 100) > 50:
            # new_point = (randint(-100, 100), randint(-100, 100))
            new_point = sample_point(points[i], sigma)
            points[i] = new_point
            #points[index] = tuple(map(operator.add, points[index], delta))
    return points


def sample_point(point, sigma):
    x = random.gauss(point[0], sigma)
    y = random.gauss(point[1], sigma)
    return (x, y)

def plot_windfarms(points, i, sigma):
    plt.clf()
    plt.scatter([p[0] for p in points], [p[1] for p in points])
    plt.title("i: %s, sigma: %s" %(i, sigma))
    plt.draw()

fig=plt.figure()
plt.xlim([0, 10000])
plt.ylim([0, 10000])
plt.ion()
plt.show(block=False)

def rls():
        ps = read_points()
        sigma = 1
        #ps = [sample_point((randint(0, 10000), randint(0, 10000)), sigma) for i in range(200)]
        initial_costs = float("inf")
        # initial_costs = costs(ps)
        new_costs = initial_costs
        i = 0
        plot_windfarms(ps, i, sigma)
        while (initial_costs <= new_costs):
                i += 1
                ps_modified = modify(ps, sigma)
                if complies_constraints(ps_modified):
                    print("#####")
                    plot_windfarms(ps, i, sigma)
                    new_costs = costs(ps_modified)
                    if (new_costs <= initial_costs):
                            ps = ps_modified
                            sigma = sigma * 0.5
                            plot_windfarms(ps, i, sigma)
                            print("---------------")
                    if (new_costs < initial_costs):
                            print_optimized(ps, new_costs)
                            return ps, new_costs, i
                if (i % 1000 == 0):
                    # ps = ps_modified
                    plot_windfarms(ps, i, sigma)
                    print(i, new_costs)


if __name__ == "__main__":
    rls()
