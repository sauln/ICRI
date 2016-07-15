import unittest
import pickle

import random


import src.model.CostFunction as cf 
import src.model.Matrices as mat

class stub():
    def __init__(self, x, y):
        self.xcoord = x
        self.ycoord = y

    def __str__(self):
        return "Stub ({},{})".format(self.xcoord, self.ycoord)
    
    def __repr__(self):
        return self.__str__()


class TestCostFunction(unittest.TestCase):
    def setUp(self):
        with open("data/interim/r101.p", "rb") as f: 
            self.problem = pickle.load(f)
        self.cf = cf.CostFunction(self.problem.customers)

    def test_feasiblePartition(self):
        for i in range(100):
            c = self.problem.customers[i]
            cs = list(self.problem.customers)
            cs.remove(c)
            feasible, infeasible = self.cf.partitionFeasible(c, cs)
            self.assertEqual(len(feasible)+len(infeasible), len(self.problem.customers)-1)

    def test_feasibleIsFeasible(self):
        for i in range(100):
            c = self.problem.customers[i]
            cs = list(self.problem.customers)
            cs.remove(c)
            feasible, infeasible = self.cf.partitionFeasible(c, cs)
           
            for f in feasible:
                c.dueDate <= f.readyTime

if __name__ == "__main__":
    unittest.main()

