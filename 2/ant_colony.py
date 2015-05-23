import xml.etree.ElementTree as ET
import networkx as nx
import collections
import random
import math
import time
import csv
import os


class Parser:
    def __init__(self, location):
            self.location = location
            self.__graph = None
            self.__optimal_solution = None

    def graph(self):
        if (self.__graph is None):
            self.__graph = nx.Graph()
            tree = ET.parse("./%s.xml" % self.location)
            vertices = tree.getroot().findall('.//vertex')
            for i in range(len(vertices)):
                vertex = vertices[i]
                edges = vertex.findall('.//edge')
                for edge in edges:
                    self.__graph.add_edge(i, int(edge.text),
                                          weight=float(edge.attrib['cost']),
                                          pheromone=0.0)
        return self.__graph

    def optimal_solution(self, location):
        START_NODE_LIST = 5

        if(self.__optimal_solution is None):
            with open("./%s.opt.tour" % location) as f:
                lines = f.readlines()
                nodes = lines[START_NODE_LIST:-2]
                nodes = [int(n.strip()) for n in nodes]
                shifted_nodes = collections.deque(nodes)
                shifted_nodes.rotate(1)
                self.__optimal_solution = nx.Graph(zip(shifted_nodes, nodes))
        return self.__optimal_solution


class Solver(object):
    def __init__(self, location, optimum=None, RHO=None, ALPHA=1, BETA=0):
        parser = Parser(location)
        self.graph = parser.graph()
        if RHO is None:
            self.RHO = 1.0/self.graph.number_of_nodes()
        else:
            self.RHO = RHO
        self.TAU_MIN = 1.0/len(self.graph.nodes())
        self.TAU_MAX = 1-self.TAU_MIN
        self.ALPHA   = ALPHA
        self.BETA    = BETA
        self.best_known_solution = []
        if optimum is None:
            optimal_path = parser.optimal_solution(location)
            self.optimum = self.tsp(optimal_path)
        else:
            self.optimum = optimum
        self.create_logfile(location)

    def find_optimum(self):
        """
        Intended to be the main interface method
        """
        self.init_pheromones()
        self.best_known_solution = self.construct()
        self.update_pheromones()
        iterations = 0
        self.t0 = time.time()
        best_cost = self.tsp(self.best_known_solution)
        self.log(best_cost, iterations)
        PRECISION = 1.05
        while (best_cost > PRECISION * self.optimum) and time.time()-self.t0 < 10*60:
                iterations = iterations + 1
                new_path = self.construct()
                if (self.tsp(new_path) < best_cost):
                        self.best_known_solution = new_path
                        best_cost = self.tsp(self.best_known_solution)
                        self.log(best_cost, iterations)
                self.update_pheromones()
        return (self.best_known_solution.edges(), iterations)

    def construct(self):
        """
        Generates a solution based on weights and current pheromone values
        """
        path  = nx.Graph()
        remaining_nodes = list(self.graph.nodes())
        first_node = self.graph.nodes()[0]
        current_node = first_node
        remaining_nodes.remove(current_node)
        while (len(remaining_nodes) != 0):
                node = self.pick_a_node(current_node, remaining_nodes)
                path.add_edge(current_node, node)
                remaining_nodes.remove(node)
                current_node = node
        path.add_edge(current_node, first_node) # close the loop
        return path

    def tsp(self, path):
        return sum([self.graph[u][v]['weight'] for u,v in path.edges()])

    def pheromone(self, edge):
        if edge in self.best_known_solution:
            return min((1 - self.RHO) * edge['pheromone'] + self.RHO, self.TAU_MAX)
        else:
            return max((1 - self.RHO) * edge['pheromone'], self.TAU_MIN)

    def init_pheromones(self):
        for (u, v) in self.graph.edges():
            self.graph[u][v]['pheromone'] = 1.0/self.graph.number_of_nodes()
        return self.graph

    def update_pheromones(self):
        for u,v in self.graph.edges():
                self.graph[u][v]['pheromone'] = self.pheromone(self.graph[u][v])

    def big_R(self, node):
        return sum([self.small_r(node, n) for n in self.graph.neighbors(node)])

    def small_r(self, node, other_node):
        tau = self.pheromone(self.graph[node][other_node])
        w = self.graph[node][other_node]['weight']
        return math.pow(tau, self.ALPHA)*math.pow(w, - self.BETA)

    def pick_a_node(self, current_node, remaining_nodes):
        choices = {}
        for n in remaining_nodes:
                probability = self.small_r(current_node, n)/self.big_R(current_node)
                choices[n] = probability
        return self.weighted_choice(choices)

    # source: http://stackoverflow.com/questions/3679694/a-weighted-version-of-random-choice
    def weighted_choice(self, choices):
        total = sum(choices.values())
        r = random.uniform(0, total)
        upto = 0
        for c, w in choices.items():
            if upto + w > r:
                return c
            upto += w
        assert False, "Shouldn't get here"

    def create_logfile(self, location):
        parameters = "RHO-%.3f_ALPHA-%.3f_BETA-%.3f" % (self.RHO, self.ALPHA, self.BETA)
        folder = "results/%s_%s" % (location, parameters)
        if not os.path.exists(folder):
            os.makedirs(folder)
        iteration = len(os.listdir(folder))
        self.filename = "%s/%s.txt" % (folder, iteration)

    def log(self, best_cost, iterations):
        with open(self.filename, "a") as f:
            row = (time.time()-self.t0, best_cost, iterations)
            csv.writer(f).writerow([int(x) for x in row])
