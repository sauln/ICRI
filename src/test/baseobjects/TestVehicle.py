import unittest
import pickle

from src import Cost, Vehicle, Customer, Point, Parameters, SolomonProblem
import src.test.Stub

class TestVehicle(unittest.TestCase):
    def setUp(self):
        self.depot   = Customer(0, Point(0, 0),  0, 0, 1000, 0)
        self.earlyC  = Customer(1, Point(0, 0),  5, 0, 10, 3)
        self.middleC = Customer(3, Point(10,10), 60, 45,75, 9)
        self.lateC   = Customer(2, Point(5, 5),  35, 99, 200, 4)
        self.customers = [self.depot, self.earlyC, self.lateC, self.middleC]
    
    def testNoCapacityFirstCustomer(self):
        for c in self.customers:
            r = Vehicle(c, 100)
            self.assertEqual(r.cur_capacity, 0)

    def testNotFull(self):
        vehicle = Vehicle(self.middleC, 100)
        self.assertTrue(vehicle.is_not_full(self.lateC), "There is plenty of room left")
        vehicle.max_capacity = 3
        self.assertFalse(vehicle.is_not_full(self.lateC), "There is enough room left")
        
    def testEqualCapacityIsOkay(self):
        vehicle = Vehicle(self.middleC, 100)
        vehicle.max_capacity = self.lateC.demand 
        self.assertTrue(vehicle.is_not_full(self.lateC), \
            "There is equal demand and not valid")

    def testTimeAfter(self):
        r = Vehicle(self.middleC, 100)
        t = r.is_valid_time(self.lateC)
        self.assertTrue(t, "Later time is valid after an early time")
        
        r.serve(self.lateC)
        f = r.is_valid_time(self.middleC)
        self.assertFalse(f, "Early time is not valid after a late time")

    def testIsFeasible(self):
        r = Vehicle(self.middleC, 100) 
        self.assertTrue(r.isFeasible(self.lateC))
        self.assertFalse(r.isFeasible(self.earlyC))

    def testAppendIncreasesCapacity(self):
        r = Vehicle(self.depot, 100)
        self.assertEqual(r.cur_capacity, 0, "doesn't start at zero")
        r.serve(self.middleC)
        self.assertEqual(r.cur_capacity, self.middleC.demand)
        r.serve(self.lateC)
        self.assertEqual(r.cur_capacity, self.middleC.demand + self.lateC.demand)
  
    def testAppendOnlyIfRoom(self):
        r = Vehicle(self.earlyC, 25)
        self.assertRaises(AssertionError, r.serve, self.lateC)

    def testConstructorAddsAllElements(self):
        r = Vehicle(self.depot, 100)
        r.serve(self.middleC)
        r.serve(self.lateC)
        self.assertEqual(len(r), 3)
        r = Vehicle(self.earlyC, 100)
        self.assertEqual(len(r), 1)

if __name__ == "__main__":
    unittest.main()

