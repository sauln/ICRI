import unittest
import pickle

from src.main.BaseObjects.Vehicle import Vehicle
from src.main.BaseObjects.Customer import Customer
from src.main.BaseObjects.SolomonProblem import SolomonProblem
from src.main.BaseObjects.Parameters import Parameters

from src.main.Algorithms.CostFunction import Cost

class TestCostFunction(unittest.TestCase):
    def setUp(self):
        self.depot   = Customer(0, 0, 0, 20, 0, 200, 0)
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

        customers = [self.depot, self.lateC, self.middleC, 
                     self.a, self.b, self.c, self.d, 
                     self.e, self.f, self.g, self.h]
        self.sp = SolomonProblem("test", 7, 100, customers)       
       
        parameters = Parameters()
        parameters.build(self.sp, 10,10)

    def iterateOverCustomers(self, func):
        vehicle = Vehicle(self.depot)
    
        for cust in self.sp.customers:
            if(vehicle.isFeasible(cust)):
                cost = func(vehicle, cust)
                self.assertGreaterEqual(cost, 0, \
                    "\n{}  ->  {} costs {}".format(vehicle.last(), cust, cost)) 
        
    @unittest.skip("Unsure of how to test this so far")
    def testCostOfRoutes(self):
        pass     

    def testCostOfDistanceOnly(self):
        self.iterateOverCustomers(Cost.distanceOnly)

    def testCostOfVehicleToCustomer(self):
        self.iterateOverCustomers(Cost.vehicleToCustomer) 

    def testGnnhIsPositive(self):
        def closedGNNH(vehicle, end):
            return Cost.gnnh([1]*7, vehicle, end)

        self.iterateOverCustomers(closedGNNH)

if __name__ == "__main__":
    unittest.main()

