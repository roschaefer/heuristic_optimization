import ant_colony
import pytest

class TestParser:
    @pytest.fixture
    def parser(self):
        return ant_colony.Parser('test_graph.xml')

    @pytest.fixture
    def nodes(self, parser):
        return parser.graph().nodes()

    @pytest.fixture
    def edges(self, parser):
        return parser.graph().edges()

    @pytest.fixture
    def graph(self, parser):
        return parser.graph()

    def test_number_of_nodes(self, parser):
        assert len(parser.graph().nodes()) == 3

    def test_edge_weight(self, parser, graph, nodes):
        assert graph.weight(nodes[0], nodes[1]) == 8.3
        assert graph.weight(nodes[2], nodes[1]) == 4.0
        assert graph.weight(nodes[2], nodes[0]) == 9.3

    def test_is_symmetric_graph(self, graph):
        assert graph.weight(nodes[2], nodes[1]) == 4.0
        assert graph.weight(nodes[1], nodes[2]) == 4.0
        assert graph.weight(nodes[0], nodes[1]) == 8.3
        assert graph.weight(nodes[1], nodes[0]) == 8.3

    def test_initial_edge_pheromones(self, edges):
        assert all(edge.pheromone() == 0 for edge in edges)

    def test_is_complete_graph(self, nodes):
        assert nodes[0].neighbors() == [nodes[1], nodes[2]]
        assert nodes[1].neighbors() == [nodes[0], nodes[2]]
        assert nodes[2].neighbors() == [nodes[0], nodes[1]]



