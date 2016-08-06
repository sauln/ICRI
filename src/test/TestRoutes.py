import unittest

from src.main.SolomonProblem import SolomonProblem
from src.main.Customer import Customer
from src.main.Routes import Routes
from src.main.CostFunction import CostFunction
from src.main.Heuristic import Heuristic
#from src.main.Matrices import Matrices

from src.main.Parameters import Parameters

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.depot   = Customer(0,  0,   0,  0,  0, 230, 0)
        self.lateC   = Customer(1,  5,   5, 20, 99, 200, 4)
        self.middleC = Customer(2, 10,  10, 20, 45,  55, 9)

        self.a       = Customer(3,  1,  10, 20,  0,  20, 3)
        self.b       = Customer(4,  2,   5, 20, 99, 200, 4)
        self.c       = Customer(5, 30,  10, 20, 45,  55, 9)
        self.d       = Customer(6,  6,  10, 20,  0,  20, 3)
        self.e       = Customer(7, 10,   5, 20, 99, 200, 4)
        self.f       = Customer(8, 25,  10, 20, 45,  55, 9)
        self.g       = Customer(9, 10,   5, 20, 99, 200, 4)
        self.h       = Customer(10,25,  10, 20, 45,  55, 9)

        customers = [self.depot, self.lateC, self.middleC, 
                             self.a, self.b, self.c, self.d, 
                             self.e, self.f, self.g, self.h]
      
        self.sp = SolomonProblem("test", 7, 100, customers)       

        params = Parameters()
        params.build(self.sp, 10,10)

        self.routes = Routes(self.depot)
        self.costFunction = CostFunction('gnnh')
    
    def testNextNodesAreFeasible(self):
        nextNodes = self.routes.getBestNNodes(self.costFunction, \
            [1]*7, self.sp.customers, 5)
        for v, c, cost in nextNodes:
            self.assertTrue(v.isFeasible(c), "{} is infeasible on {}".format(c,v))

    def testNextNodesAreAscendingOrder(self):
        nextNodes = self.routes.getBestNNodes(self.costFunction, \
            [1]*7, self.sp.customers, 5)

        for i in range(len(nextNodes) - 1):
            vehiclel, custl, costl = nextNodes[i]
            vehicler, custr, costr = nextNodes[i+1]
            self.assertLessEqual(costl, costr)
    
    def testTopNodeIsMaxOfNNodes(self):
        nextNodes = self.routes.getBestNNodes(self.costFunction, \
            [1]*7, self.sp.customers,5)

        nt = min(nextNodes, key = lambda x: x[2])
        top = self.routes.getBestNode(self.costFunction, \
            [1]*7, self.sp.customers)

        self.assertEqual(top, nt)

    def testNNodesIsRightSize(self):
        nextNodes = self.routes.getBestNNodes(self.costFunction, \
            [1]*7, self.sp.customers,5)
        self.assertEqual(len(nextNodes), 5)

        nextNodes = self.routes.getBestNNodes(self.costFunction, \
            [1]*7, self.sp.customers,1)
        self.assertEqual(len(nextNodes), 1)
        
        tmp_customers = list(self.sp.customers)
        tmp_customers.remove(self.depot)
       
        feasibleNodes = [c for c in self.sp.customers if self.routes[0].isFeasible(c)]
        nextNodes = self.routes.getBestNNodes(self.costFunction, \
            [1]*7, self.sp.customers,99)
       
        self.assertEqual(len(nextNodes), len(feasibleNodes), \
            "\nnextNoodes: {}\nfeasible nodes:{}".format(nextNodes, feasibleNodes))

if __name__ == "__main__":
    unittest.main()

