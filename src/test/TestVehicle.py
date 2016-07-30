import unittest
import pickle

from src.main.SolomonProblem import SolomonProblem
from src.main.Customer import Customer
from src.main.Routes import Routes
from src.main.Vehicle import Vehicle
from src.main.Customer import Customer
from src.main.Matrices import Matrices


class TestVehicle(unittest.TestCase):
    def setUp(self):
        self.sp = SolomonProblem("test", 5, 1000, None)
        
        earlyC  = Customer(0, 0,  0,  5, 0, 10, 3)
        lateC   = Customer(1, 5,  5, 35, 99, 200, 4)
        middleC = Customer(2, 10,10, 60, 45,75, 9)

        self.earlyC, self.lateC, self.middleC = earlyC, lateC, middleC 
        
        self.sp.customers = [earlyC, lateC, middleC]
        
        m = Matrices()
        m.build(self.sp.customers)
        self.r = Vehicle(self.sp, earlyC, lateC)
    
    def testNotFull(self):
        vehicle = Vehicle(self.sp, self.middleC)
        t = vehicle.isNotFull(self.lateC)
        self.assertTrue(t, "There is plenty of room left")

        vehicle.maxCapacity = 25
        f = vehicle.isNotFull(self.lateC)
        self.assertFalse(f, "There is not enough room left")

    def testTimeAfter(self):
        r = Vehicle(self.sp, self.middleC)
        t = r.isValidTime(self.lateC)
        self.assertTrue(t, "Later time is valid after an early time")
        
        self.r.append(self.lateC)
        f = self.r.isValidTime(self.middleC)
        self.assertFalse(f, "Early time is not valid after a late time")

    def testIsFeasible(self):
        r = Vehicle(self.sp, self.middleC) 
        t = r.isFeasible(self.lateC)
        self.assertTrue(t)
        f = r.isFeasible(self.earlyC)
        self.assertFalse(f)

    def testAppendIncreasesCapacity(self):
        r = Vehicle(self.sp, self.earlyC)
        r.append(self.middleC)
        self.assertEqual(r.curCapacity, self.middleC.demand)

        r.append(self.lateC)
        self.assertEqual(r.curCapacity, self.middleC.demand + self.lateC.demand)
  
    def testAppendOnlyIfRoom(self):
        self.sp.capacity = 25
        r = Vehicle(self.sp, self.earlyC)
        self.assertRaises(AssertionError, r.append, self.lateC)
        self.assertRaises(AssertionError, Vehicle, self.sp, self.lateC, self.middleC) 

    def testConstructorAddsAllElements(self):
        r = Vehicle(self.sp, self.earlyC, self.middleC, self.lateC)
        self.assertEqual(len(r), 3)
        r = Vehicle(self.sp, self.earlyC, self.earlyC)
        self.assertEqual(len(r), 2)

    @unittest.skip("Instead asserting that __setitem__ is never called")
    def testFixCapacityOnReplace(self):
        r = Vehicle(self.sp, self.earlyC, self.middleC)
        self.assertEqual(r.curCapacity, self.earlyC.demand + self.middleC.demand)
        r[0] = self.lateC
        self.assertEqual(r.curCapacity, self.lateC.demand + self.middleC.demand)
        r[1] = self.earlyC
        self.assertEqual(r.curCapacity, self.lateC.demand + self.earlyC.demand)

if __name__ == "__main__":
    unittest.main()

