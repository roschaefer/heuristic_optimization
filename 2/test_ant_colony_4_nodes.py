import ant_colony
import pytest
import networkx as nx


class TestSolver:

    TEST_PROBLEM = 'test/test_graph_4_nodes'
    TAU_MAX = 2/3.0
    TAU_MIN = 1/3.0

    @pytest.fixture
    def solver(self):
        return ant_colony.Solver(self.TEST_PROBLEM)

    @pytest.fixture
    def edge(self, solver):
        return solver.graph.edge[0][1]

    def test_find_optimum_terminates(self, solver):
        optimal_path, _ = solver.find_optimum()
        expected = nx.Graph([(0,1),(1,3), (3,2), (2,0)])
        assert optimal_path == expected.edges()
        assert solver.tsp(solver.best_known_solution) == 4

    def test_big_R(self, solver):
        solver.init_pheromones()
        solver.ALPHA = 1
        solver.BETA  = -1
        expected = (1.0 + 1.0 + 4.0)/4.0 # sum of costs = 6, number of nodes = 4
        assert solver.big_R(0) == expected
