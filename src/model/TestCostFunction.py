import unittest
import pickle

import src.model.CostFunction as cf 



class TestMatrices(unittest.TestCase):
    def setUp(self):
        self.customers = [stub(a,b) for a,b in zip(range(5), range(5))] 
        self.problem = mat.SolomonProblem("test", 5,5, self.customers) 
        self.m = mat.Matrices(self.customers)





if __name__ == "__main__":
    unittest.main()

