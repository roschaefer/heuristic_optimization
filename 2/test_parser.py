import ant_colony
import pytest
from IPython import embed


class TestParser:
    @pytest.fixture
    def parser(self):
        return ant_colony.Parser('test/test_graph')

    @pytest.fixture
    def nodes(self, parser):
        return parser.graph().nodes()

    @pytest.fixture
    def edges(self, parser):
        return parser.graph().edges()

    @pytest.fixture
    def graph(self, parser):
        return parser.graph()

    def test_number_of_nodes(self, nodes):
        assert len(nodes) == 3

    def test_edge_weight(self, graph):
        assert graph.edge[0][1]['weight'] == 83
        assert graph.edge[2][1]['weight'] == 40
        assert graph.edge[2][0]['weight'] == 93

    def test_is_symmetric_graph(self, graph):
        assert graph.edge[2][1]['weight'] == 40
        assert graph.edge[1][2]['weight'] == 40
        assert graph.edge[0][1]['weight'] == 83
        assert graph.edge[1][0]['weight'] == 83

    def test_initial_edge_pheromones(self, graph, edges):
        assert all(graph[u][v]['pheromone'] == 0 for (u, v) in edges)

    def test_is_complete_graph(self, graph):
        assert list(graph[0].keys()) == [1, 2]
        assert list(graph[1].keys()) == [0, 2]
        assert list(graph[2].keys()) == [0, 1]

    def test_loads_optimal_solution(self, parser):
        solution = parser.optimal_solution('test/test_graph')
        assert solution.edges() == [(0, 2), (1, 2)]
