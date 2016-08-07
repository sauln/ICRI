import unittest
import pickle

from src.main.SolomonProblem import SolomonProblem
from src.main.Customer import Customer
from src.main.Vehicle import Vehicle
from src.main.CostFunction import CostFunction
from src.main.Parameters import Parameters
from src.main.Routes import Routes



class TestCostFunction(unittest.TestCase):
    def setUp(self):
        self.earlyC  = Customer(0, 0, 0, 20, 0, 200, 0)
        self.lateC   = Customer(1, 5, 5, 20, 99, 200, 4)
        self.middleC = Customer(2, 10,10, 20, 45,55, 9)
        self.a = Customer(3, 1,  10, 20,  0,  20, 3)
        self.b = Customer(4, 2,   5, 20, 99, 200, 4)
        self.c = Customer(5, 30, 10, 20, 45,  55, 9)
        self.d = Customer(6, 6,  10, 20,  30,  40, 3)
        self.e = Customer(7, 10,  5, 20, 99, 200, 4)
        self.f = Customer(8, 25, 10, 20, 45,  55, 9)
        self.g = Customer(9, 10,  5, 20, 99, 200, 4)
        self.h = Customer(10, 25, 10, 20, 45,  55, 9)
        self.depot = self.earlyC

        customers = [self.earlyC, self.lateC, self.middleC, 
                             self.a, self.b, self.c, self.d, 
                             self.e, self.f, self.g, self.h]
        self.sp = SolomonProblem("test", 7, 100, customers)       
       
        parameters = Parameters()
        parameters.build(self.sp, 10,10)
        self.costFunction = CostFunction('gnnh')
        self.routes = Routes(self.depot)

    def testCostFunctionIsPositive(self):
        vehicle = Vehicle(self.earlyC)
    
        cf = CostFunction("gnnh")
        for cust in self.sp.customers:
            if(vehicle.isFeasible(cust)):
                cost = cf.run([1]*7, vehicle, cust)
                self.assertGreaterEqual(cost, 0, \
                    "\n{}  ->  {} costs {}".format(vehicle.last(), cust, cost)) 
   
    def testNextNodesAreFeasible(self):
        nextNodes = self.costFunction.getBestNNodes(\
            [1]*7, self.routes.last(), self.sp.customers, 5)
        for v in nextNodes:
            self.assertTrue(v.vehicle.isFeasible(v.customer), \
                "{} feasibility".format(v.vehicle.feasibilityStr(v.customer)))

    #def getBestNNodes(self, delta, vehicle, customers, size):
    def testNextNodesAreAscendingOrder(self):
        nextNodes = self.costFunction.getBestNNodes(\
            [1]*7, self.routes.last(), self.sp.customers, 5)

        for i in range(len(nextNodes) - 1):
            self.assertLessEqual(nextNodes[i].gnnhCost, nextNodes[i+1].gnnhCost)
    
    def testTopNodeIsMaxOfNNodes(self):
        # def getBestNNodes(self, delta, vehicle, customers, size):

        nextNodes = self.costFunction.getBestNNodes([1]*7, self.routes.last(),\
                                                    self.sp.customers, 5)

        nt = min(nextNodes, key = lambda x: x.gnnhCost)
        top = self.costFunction.getBestNode([1]*7, self.routes.last(), self.sp.customers)

        self.assertEqual(top, nt, "\n{} != \n{}".format(nt, top))

    def testNNodesIsRightSize(self):
        nextNodes = self.costFunction.getBestNNodes(\
            [1]*7, self.routes.last(), self.sp.customers, 5)
        self.assertEqual(len(nextNodes), 5)

        nextNodes = self.costFunction.getBestNNodes(\
            [1]*7, self.routes.last(), self.sp.customers, 1)
        self.assertEqual(len(nextNodes), 1)
        
        #tmp_customers = list(self.sp.customers)
        #tmp_customers.remove(self.depot)
       
        #feasibleNodes = [c for c in self.sp.customers if self.routes.last().isFeasible(c)]
        #nextNodes = self.costFunction.getBestNNodes(\
        #    [1]*7, self.routes.last(), self.sp.customers, 99)
       
        #self.assertEqual(len(nextNodes), len(feasibleNodes), \
        #    "\nnextNoodes: {}\nfeasible nodes:{}".format(nextNodes, feasibleNodes))

if __name__ == "__main__":
    unittest.main()

