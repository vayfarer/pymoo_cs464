import unittest

import numpy as np

from pymoo.algorithms.nsga2 import nsga2
from pymoo.factory import get_problem, Problem, ZDT
from pymoo.optimize import minimize


class AlgorithmTest(unittest.TestCase):

    def test_same_seed_same_result(self):
        problem = get_problem("zdt3")
        algorithm = nsga2(pop_size=100, elimate_duplicates=True)

        res1 = minimize(problem, algorithm, ('n_gen', 20), seed=1)
        res2 = minimize(problem, algorithm, ('n_gen', 20), seed=1)

        self.assertEqual(res1.X.shape, res2.X.shape)
        self.assertTrue(np.all(np.allclose(res1.X, res2.X)))

    def test_no_pareto_front_given(self):
        class ZDT1NoPF(ZDT):
            def _evaluate(self, x, out, *args, **kwargs):
                f1 = x[:, 0]
                g = 1 + 9.0 / (self.n_var - 1) * np.sum(x[:, 1:], axis=1)
                f2 = g * (1 - np.power((f1 / g), 0.5))
                out["F"] = np.column_stack([f1, f2])

        algorithm = nsga2(pop_size=100, elimate_duplicates=True)
        minimize(ZDT1NoPF(), algorithm, ('n_gen', 20), seed=1, verbose=True)


if __name__ == '__main__':
    unittest.main()
