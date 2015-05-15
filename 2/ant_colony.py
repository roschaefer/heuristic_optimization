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
            tree = ET.parse("./%s" % self.location)
            vertices = tree.getroot().findall('.//vertex')
            for i in range(len(vertices)):
                vertex = vertices[i]
                self.__graph.add_node(i)
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
