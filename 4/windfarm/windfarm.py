#!/usr/bin/env python
import optunity
import math
import operator
from IPython import embed
import subprocess
from random import randint
import random


def points_formatted(points):
    return '\n'.join([' '.join(map(str,p)) for p in points])

def print_points(points, cost):
    with open('optimized.dat', 'w') as the_file:
            the_file.write(str(len(points)))
            the_file.write('\n')
            the_file.write(points_formatted(points))
            the_file.write('\n')
    with open('optimized.val', 'w') as the_file:
            the_file.write(str(cost))

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

def costs(points):
    print_points(points, 0)
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


def modify(points):
        points = points.copy()
        index = randint(0, len(points)-1)
        delta = (randint(-100,100), randint(-100,100))
        points[index] = tuple(map(operator.add, points[index], delta))
        return points

def modify_gauss(points, sigma):
        points = points.copy()
        index = randint(0, len(points)-1)
        p = sample_gauss(points[index], sigma)
        points[index] = p
        return points

def sample_gauss(point, sigma):
    x = random.gauss(point[0], sigma)
    y = random.gauss(point[1], sigma)
    return x, y

def rls_gauss():
        ps = read_points()
        initial_costs = costs(ps)
        new_costs = best_cost = initial_costs
        print("### initial cost: ", initial_costs)
        i = 0
        sigma = 1000
        while (i < 500):
                i += 1
                ps_modified = modify_gauss(ps, sigma)
                new_costs = costs(ps_modified)
                if (new_costs < initial_costs):
                        ps = ps_modified
                        best_cost = new_costs
                        print_points(ps, best_cost)
                        sigma = sigma * 0.7
                # if (new_costs < initial_costs):
                #         # return ps, new_costs, i
                #         break
                if (i % 100 == 0):
                    print(i)
        print(ps, i, sigma, best_cost)
        return ps, best_cost


def rls():
        ps = read_points()
        initial_costs = costs(ps)
        new_costs = best_cost = initial_costs
        print("### initial cost: ", initial_costs)
        i = 0
        while (i < 500):
                i += 1
                ps_modified = modify(ps)
                new_costs = costs(ps_modified)
                if (new_costs < initial_costs):
                        ps = ps_modified
                        best_cost = new_costs
                        print_points(ps, best_cost)
                # if (new_costs < initial_costs):
                #         # return ps, new_costs, i
                #         break
                if (i % 100 == 0):
                    print(i)
        print(ps, i, best_cost)
        return ps, best_cost

if __name__ == '__main__':
    rls_gauss()
