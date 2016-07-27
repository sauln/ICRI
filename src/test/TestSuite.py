import unittest

from src.test.TestMatrices import TestMatrices
from src.test.TestSolomonProblem import TestSolomonProblem
from src.test.TestCustomer import TestCustomer
from src.test.TestVehicle import TestVehicle
from src.test.TestHeuristic import TestHeuristic
from src.test.TestRoutes import TestRoutes




if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMatrices)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRoutes)
    unittest.TextTestRunner(verbosity=2).run(suite)

