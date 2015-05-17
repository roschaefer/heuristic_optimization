import xml.etree.ElementTree as ET
import networkx as nx
import collections
import random


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
    def __init__(self, location):
        parser = Parser(location)
        self.optimal_solution = parser.optimal_solution(location)
        self.graph = parser.graph()
        self.RHO = 1.0/self.graph.number_of_nodes()
        self.TAU_MIN = 1.0/len(self.graph.nodes())
        self.TAU_MAX = 1-self.TAU_MIN
        self.best_known_solution = []

    def find_optimum(self):
        """
        Intended to be the main interface method
        """
        self.init_pheromones()
        self.best_known_solution = self.construct()
        self.update_pheromones()
        optimum = self.tsp(self.optimal_solution)
        while (self.tsp(self.best_known_solution) > optimum):
                new_path = self.construct()
                if (self.tsp(new_path) < self.tsp(self.best_known_solution)):
                        self.best_known_solution = new_path
                self.update_pheromones()
        return self.best_known_solution.edges()

    def construct(self):
        """
        Generates a solution based on weights and current pheromone values
        """
        nodes = self.graph.nodes().copy()
        random.shuffle(nodes)
        shifted_nodes = collections.deque(nodes)
        shifted_nodes.rotate(1)
        path  = nx.Graph(zip(shifted_nodes, nodes))
        return path

    def tsp(self, path):
        costs = 0
        for u,v in path.edges():
                costs += self.graph[u][v]['weight']
        return costs

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

