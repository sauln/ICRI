import unittest
import pickle

from src.main.SolomonProblem import SolomonProblem
from src.main.Customer import Customer
from src.main.Vehicle import Vehicle
from src.main.Customer import Customer
from src.main.Parameters import Parameters


class TestVehicle(unittest.TestCase):
    def setUp(self):
        self.depot   = Customer(0, 0,  0,  0, 0, 1000, 0)
        self.earlyC  = Customer(1, 0,  0,  5, 0, 10, 3)
        self.lateC   = Customer(2, 5,  5, 35, 99, 200, 4)
        self.middleC = Customer(3, 10,10, 60, 45,75, 9)
        customers = [self.depot, self.earlyC, self.lateC, self.middleC]
        param =  SolomonProblem("test", 5, 1000, customers)

        self.sp = Parameters()
        self.sp.build(param, 10, 10)

    def testNotFull(self):
        vehicle = Vehicle(self.middleC)
        t = vehicle.isNotFull(self.lateC)
        self.assertTrue(t, "There is plenty of room left")

        vehicle.maxCapacity = 25
        f = vehicle.isNotFull(self.lateC)
        self.assertFalse(f, "There is not enough room left")

    def testTimeAfter(self):
        r = Vehicle(self.middleC)
        t = r.isValidTime(self.lateC)
        self.assertTrue(t, "Later time is valid after an early time")
        
        r.append(self.lateC)
        f = r.isValidTime(self.middleC)
        self.assertFalse(f, "Early time is not valid after a late time")

    def testIsFeasible(self):
        r = Vehicle(self.middleC) 
        self.assertTrue(r.isFeasible(self.lateC))
        self.assertFalse(r.isFeasible(self.earlyC))

    def testAppendIncreasesCapacity(self):
        r = Vehicle(self.earlyC)
        self.assertEqual(r.curCapacity, self.earlyC.demand)

        r = Vehicle(self.earlyC)
        r.append(self.middleC)
        self.assertEqual(r.curCapacity, \
            self.middleC.demand + self.earlyC.demand)

        r.append(self.lateC)
        self.assertEqual(r.curCapacity, \
            self.middleC.demand + self.lateC.demand + self.earlyC.demand)
  
    def testAppendOnlyIfRoom(self):
        self.sp.params.capacity = 25
        r = Vehicle(self.earlyC)
        self.assertRaises(AssertionError, r.append, self.lateC)
        self.assertRaises(AssertionError, Vehicle, self.lateC, self.middleC) 

    def testConstructorAddsAllElements(self):
        r = Vehicle(self.earlyC, self.middleC, self.lateC)
        self.assertEqual(len(r), 3)
        r = Vehicle(self.earlyC)
        self.assertEqual(len(r), 1)

    @unittest.skip("Instead asserting that __setitem__ is never called")
    def testFixCapacityOnReplace(self):
        r = Vehicle(self.earlyC, self.middleC)
        self.assertEqual(r.curCapacity, self.earlyC.demand + self.middleC.demand)
        r[0] = self.lateC
        self.assertEqual(r.curCapacity, self.lateC.demand + self.middleC.demand)
        r[1] = self.earlyC
        self.assertEqual(r.curCapacity, self.lateC.demand + self.earlyC.demand)

if __name__ == "__main__":
    unittest.main()

