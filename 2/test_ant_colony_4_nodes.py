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

    #def test_find_optimum_terminates(self, solver):
        #optimal_path = solver.find_optimum()
        #print(optimal_path)

