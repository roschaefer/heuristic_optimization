import xml.etree.ElementTree as ET
import networkx as nx


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
                edges = [(nodes[i], nodes[i+1]) for i in range(len(nodes)-1)]
                self.__optimal_solution = nx.Graph(edges)
        return self.__optimal_solution


class Solver(object):
    def __init__(self, location):
        parser = Parser(location)
        self.optimal_solution = parser.optimal_solution(location)
        self.problem = parser.graph()
        self.graph = parser.graph()
        self.RHO = 1.0/len(self.problem.nodes())
        self.TAU_MIN = 1.0/len(self.problem.nodes())
        self.TAU_MAX = 1-self.TAU_MIN
        self.best_known_solution = []

    def find_optimum(self):
        """
        Intended to be the main interface method
        """
        self.problem = self.init_pheromones(self.problem)
        self.best_known_solution = self.construct()
        return self.best_known_solution

    def construct(self):
        """
        Generates a solution based on weights and current pheromone values
        """
        result = []
        n = len(self.graph.nodes())
        for i in range(n - 1):
                edge = (i, i+1)
                result.append(edge)
        return result

    def pheromone(self, edge):
        if edge in self.optimal_solution:
            return min((1 - self.RHO) * edge['pheromone'] + self.RHO, self.TAU_MAX)
        else:
            return max((1 - self.RHO) * edge['pheromone'], self.TAU_MIN)

    def init_pheromones(self, graph):
        for (u, v) in graph.edges():
            edge = graph[u][v]
            edge['pheromone'] = self.pheromone(edge)
        return graph

