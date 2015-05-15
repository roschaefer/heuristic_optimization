import ant_colony
import pytest


class TestSolver:

    TEST_PROBLEM = 'test/test_graph'
    TAU_MAX = 2/3.0
    TAU_MIN = 1/3.0

    @pytest.fixture
    def solver(self):
        return ant_colony.Solver(self.TEST_PROBLEM)

    @pytest.fixture
    def edge(self, solver):
        return solver.problem.edge[0][1]

    def test_solves_until_optimum(self, solver):
        assert solver.find_optimum() == [(0, 2), (1, 2)]

    def test_pheromone_for_optimal_edge_up_to_max(self, solver, edge):
        new_pheromone = solver.pheromone(edge)
        assert new_pheromone <= self.TAU_MAX

    def test_pheromone_for_other_edge_down_to_min(self, solver, edge):
        new_pheromone = solver.pheromone(edge)
        assert new_pheromone >= self.TAU_MIN
