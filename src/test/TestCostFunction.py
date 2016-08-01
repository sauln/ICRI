import unittest
import pickle

from src.main.SolomonProblem import SolomonProblem
from src.main.Customer import Customer
from src.main.Vehicle import Vehicle
from src.main.CostFunction import CostFunction
from src.main.Parameters import Parameters




class TestCostFunction(unittest.TestCase):
    def setUp(self):
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
        self.depot = self.earlyC

        customers = [self.earlyC, self.lateC, self.middleC, 
                             self.a, self.b, self.c, self.d, 
                             self.e, self.f, self.g, self.h]
        self.sp = SolomonProblem("test", 7, 100, customers)       
       
        parameters = Parameters()
        parameters.build(self.sp)

    def testCostFunctionIsPositive(self):
        vehicle = Vehicle(self.earlyC)
    
        cf = CostFunction("gnnh")
        for cust in self.sp.customers:
            if(vehicle.isFeasible(cust)):
                cost = cf.run([1]*7, vehicle, cust)
                self.assertGreaterEqual(cost, 0, \
                    "\n{}  ->  {} costs {}".format(vehicle.last(), cust, cost)) 

if __name__ == "__main__":
    unittest.main()
