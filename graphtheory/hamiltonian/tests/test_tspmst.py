#!/usr/bin/python

import unittest
from graphtheory.structures.edges import Edge
from graphtheory.structures.graphs import Graph
from graphtheory.hamiltonian.tspmst import *

# http://en.wikipedia.org/wiki/Travelling_salesman_problem
# Wagi krawedzi spelniaja warunek trojkata.
#      20                Three Hamiltonian cycles:
#   0 --- 1              0 1 3 2 = 108
#   | \ / |              0 2 1 3 = 141
# 42|  X  |34            0 1 2 3 = 97
#   | / \ |
#   2 --- 3
#      12

class TestTSP(unittest.TestCase):

    def setUp(self):
        self.N = 4
        self.G = Graph(self.N)
        self.nodes = range(self.N)
        self.edges = [
            Edge(0, 1, 20), Edge(0, 3, 35), Edge(0, 2, 42), 
            Edge(1, 2, 30), Edge(1, 3, 34), Edge(2, 3, 12)]
        for node in self.nodes:
            self.G.add_node(node)
        for edge in self.edges:
            self.G.add_edge(edge)
        self.best_weight = 97
        #self.G.show()

    def test_prim_tsp_with_edges(self):
        algorithm = PrimTSPWithEdges(self.G)
        algorithm.run(0)
        weight = sum(edge.weight for edge in algorithm.hamiltonian_cycle)
        self.assertEqual(weight, self.best_weight)

    def test_prim_tsp_with_cycle_graph(self):
        algorithm = PrimTSPWithGraph(self.G)
        algorithm.run(0)
        weight = sum(edge.weight for edge in algorithm.hamiltonian_cycle.iteredges())
        self.assertEqual(weight, self.best_weight)
        #algorithm.hamiltonian_cycle.show()
        self.assertEqual(algorithm.hamiltonian_cycle.e(),
                         algorithm.hamiltonian_cycle.v())
        for node in algorithm.hamiltonian_cycle.iternodes():
            self.assertEqual(algorithm.hamiltonian_cycle.degree(node), 2)

    def test_exceptions(self):
        self.assertRaises(ValueError, PrimTSPWithEdges, Graph(5, True))
        self.assertRaises(ValueError, PrimTSPWithGraph, Graph(5, True))

    def tearDown(self): pass

if __name__ == "__main__":

    unittest.main()

# EOF
