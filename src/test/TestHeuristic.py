import unittest
import pickle

from src.main.SolomonProblem import SolomonProblem
from src.main.Customer import Customer
from src.main.Routes import Routes
from src.main.Vehicle import Vehicle
from src.main.CostFunction import CostFunction

from src.main.basicOps import *

class TestHeuristic(unittest.TestCase):
    def setUp(self):
        self.sp = SolomonProblem("test", 7, 100, None)       
        #routes = gnnh.buildSolution(delta, depot, customers, depot)


        self.earlyC  = Customer(0, 0, 0, 20, 0, 10, 3)
        self.lateC   = Customer(1, 5, 5, 20, 99, 200, 4)
        self.middleC = Customer(2, 10,10, 20, 45,55, 9)

        self.a = Customer(3, 1,  10, 20,  0,  10, 3)
        self.b = Customer(4, 2,   5, 20, 99, 200, 4)
        self.c = Customer(5, 30, 10, 20, 45,  55, 9)
        self.d = Customer(6, 6,  10, 20,  0,  10, 3)
        self.e = Customer(7, 10,  5, 20, 99, 200, 4)
        self.f = Customer(8, 25, 10, 20, 45,  55, 9)
        self.g = Customer(9, 10,  5, 20, 99, 200, 4)
        self.h = Customer(10, 25, 10, 20, 45,  55, 9)

        self.sp.customers = [self.earlyC, self.lateC, self.middleC, 
                             self.a, self.b, self.c, self.d, 
                             self.e, self.f, self.g, self.h]
       
        self.depot = self.earlyC

        self.delta = [1]*7
        self.sp.prepare()
        self.gnnh = Heuristic(self.sp)
        self.gnnh.setup(self.delta, self.depot, self.sp.customers, self.depot) 

        self.routes = Routes(self.sp, self.earlyC)

    def testHeuristicIsPositive(self):
        vehicle = Vehicle(self.sp, self.earlyC)
    
        cf = CostFunction("gnnh", self.sp.timeMatrix, self.sp.distMatrix)
        for cust in self.sp.customers:
            cost = cf.run(self.delta, vehicle, cust)
            self.assertGreaterEqual(cost, 0) 
    
    def testNextNodesAreFeasible(self):
        nextNodes = self.gnnh.getBestNNodes(5)
        for v, c, cost in nextNodes:
            self.assertTrue(v.isFeasible(c))

    def testNextNodesAreAscendingOrder(self):
        nextNodes = self.gnnh.getBestNNodes(5)

        for i in range(len(nextNodes) - 1):
            vehiclel, custl, costl = nextNodes[i]
            vehicler, custr, costr = nextNodes[i+1]
            self.assertLessEqual(costl, costr)
    
    def testTopNodeIsMaxOfNNodes(self):
        nextNodes = self.gnnh.getBestNNodes(5)

        nt = min(nextNodes, key = lambda x: x[2])
        top = self.gnnh.getBestNode()

        self.assertEqual(top, nt)

    def testNNodesIsRightSize(self):
        nextNodes = self.gnnh.getBestNNodes(5)
        self.assertEqual(len(nextNodes), 5)

        nextNodes = self.gnnh.getBestNNodes(1)
        self.assertEqual(len(nextNodes), 1)
        
        tmp_customers = list(self.sp.customers)
        tmp_customers.remove(self.depot)
        
        feasibleNodes = [c for c in self.gnnh.customers if self.routes[0].isFeasible(c)]
        nextNodes = self.gnnh.getBestNNodes(99)
        
        self.assertEqual(len(nextNodes), len(feasibleNodes), \
            "\nnextNoodes: {}\ncustomers:{}".format(nextNodes, feasibleNodes))


if __name__ == "__main__":
    unittest.main()
