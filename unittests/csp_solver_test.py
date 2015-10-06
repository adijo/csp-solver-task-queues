import unittest
import os.path,sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

import csp_solver

class CSPSolverTest(unittest.TestCase):
    def __init__(self):
        self.solver = csp_solver.CSPSolver()

    def correctness_test(self):
        graph = [('a', 'b'), ('b', 'c'), ('a', 'd'), ('b', 'd'), ('c', 'd'), ('c', 'e'), ('d', 'e'), ('d', 'f'), ('e', 'f')]
        variables = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        domains = [0, 1, 2]
        unary = {x : set() for x in variables}
        res = solver.solve(graph, variables, domains, unary)
        expected = (True, {'a': 0, 'c': 0, 'b': 1, 'e': 1, 'd': 2, 'g': 0, 'f': 0})

        assertEquals(res, expected)

    
if __name__ == '__main__':
    unittest.main()
