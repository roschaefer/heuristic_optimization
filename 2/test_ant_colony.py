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
        assert solver.find_optimum() == [(0, 2), (2, 1)]

    def test_pheromone_for_optimal_edge_up_to_max(self, solver, edge):
        new_pheromone = solver.pheromone(edge)
        assert new_pheromone <= self.TAU_MAX

    def test_pheromone_for_other_edge_down_to_min(self, solver, edge):
        new_pheromone = solver.pheromone(edge)
        assert new_pheromone >= self.TAU_MIN

    def test_initial_pheromones(self, solver):
        graph = solver.init_pheromones(solver.problem)
        assert graph.edge[0][1]['pheromone'] == 1/3.0

    def test_sets_initial_pheromones(self, solver):
        solver.find_optimum()
        assert solver.problem.edge[0][1]['pheromone'] == 1/3.0

    def test_construct_number_of_edges(self, solver):
        graph = solver.construct()
        assert graph.number_of_edges() == 2 # not a round trip, so two edges for three nodes

    def test_construct_incoming_outcoming_edges(self, solver):
        graph = solver.construct()
        assert graph.neighbors(0) == [1]
        assert graph.neighbors(1) == [0,2]
        assert graph.neighbors(2) == [1]
