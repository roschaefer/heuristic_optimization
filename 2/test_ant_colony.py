import ant_colony
import pytest
import networkx as nx


class TestSolver:

    TEST_PROBLEM = 'test/test_graph'
    TAU_MAX = 2/3.0
    TAU_MIN = 1/3.0

    @pytest.fixture
    def solver(self):
        return ant_colony.Solver(self.TEST_PROBLEM)

    @pytest.fixture
    def edge(self, solver):
        return solver.graph.edge[0][1]

    def test_solves_until_optimum(self, solver):
        solver.find_optimum()
        graph = solver.best_known_solution
        expected =  nx.Graph( [(0, 1), (1, 2), (2, 0)])
        assert nx.is_isomorphic(graph, expected)
        #assert solver.find_optimum() == [(0, 1), (1, 2), (2, 0)]

    def test_pheromone_for_optimal_edge_up_to_max(self, solver, edge):
        new_pheromone = solver.pheromone(edge)
        assert new_pheromone <= self.TAU_MAX

    def test_pheromone_for_other_edge_down_to_min(self, solver, edge):
        new_pheromone = solver.pheromone(edge)
        assert new_pheromone >= self.TAU_MIN

    def test_initial_pheromones(self, solver):
        graph = solver.init_pheromones()
        assert graph.edge[0][1]['pheromone'] == 1/3.0

    def test_sets_initial_pheromones(self, solver):
        solver.find_optimum()
        assert solver.graph.edge[0][1]['pheromone'] == 1/3.0

    def test_construct_number_of_edges(self, solver):
        graph = solver.construct()
        assert graph.number_of_edges() == 3

    def test_construct_round_trip(self, solver):
        graph = solver.construct()
        assert graph.neighbors(0) == [1,2]
        assert graph.neighbors(1) == [0,2]
        assert graph.neighbors(2) == [0,1]

    def test_tsp(self, solver):
        path = nx.Graph()
        path.add_edge(0,2)
        path.add_edge(2,1)
        path.add_edge(1,0)
        expected = 93 + 40 + 83
        assert solver.tsp(path) == expected

    def test_construct_with_cost_of_optimal_solution(self):
        OPTIMUM = 600
        solver = ant_colony.Solver(self.TEST_PROBLEM, OPTIMUM)
        assert solver.optimum == OPTIMUM

    def test_returns_no_of_iterations(self, solver):
        (_, iterations) = solver.find_optimum()
        assert iterations == 0
