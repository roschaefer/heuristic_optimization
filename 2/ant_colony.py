import xml.etree.ElementTree as ET
import networkx as nx

class Parser:
    def __init__(self, location):
            self.location = location
            self.__graph   = None

    def graph(self):
        if (self.__graph == None):
            self.__graph = nx.Graph()
            tree = ET.parse("./%s" % self.location)
            vertices = tree.getroot().findall('.//vertex')
            for i in range(len(vertices)):
                self.__graph.add_node(i)
        return self.__graph


