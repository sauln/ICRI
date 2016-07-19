import unittest
import pickle

from src.main.SolomonProblem import SolomonProblem, Customer
from src.main.Routes import Route, Routes

class TestRoute(unittest.TestCase):
    def setUp(self):
        self.sp = SolomonProblem("test", 5, 100, None)
        
        earlyC  = Customer(0, 0,  0,  5, 0, 10, 3)
        lateC   = Customer(1, 5,  5, 35, 99, 200, 4)
        middleC = Customer(2, 10,10, 60, 45,55, 9)

        self.earlyC, self.lateC, self.middleC = earlyC, lateC, middleC 
        
        self.sp.customers = [earlyC, lateC, middleC]
        self.sp.prepare()
        r = Route(self.sp, earlyC, lateC)

    def testAppendIncreasesCapacity(self):
        r = Route(self.sp, self.earlyC)
        d = self.earlyC.demand
        self.assertEqual(r.capacity, self.earlyC.demand)

        r.append(self.lateC)
        d = self.earlyC.demand + self.lateC.demand
        self.assertEqual(r.capacity, self.earlyC.demand + self.lateC.demand)

        r.append(self.middleC)
        d = self.earlyC.demand + self.lateC.demand + self.middleC.demand
        self.assertEqual(r.capacity, d)
   
    def testAppendOnlyIfRoom(self):
        self.sp.capacity = 25
        r = Route(self.sp, self.earlyC)
        self.assertRaises(AssertionError, r.append, self.lateC)
        self.assertRaises(AssertionError, Route, self.sp, self.lateC, self.middleC) 

    def testConstructorAddsAllElements(self):
        r = Route(self.sp, self.earlyC, self.middleC, self.lateC)
        self.assertEqual(len(r), 3)
        r = Route(self.sp, self.earlyC, self.earlyC)
        self.assertEqual(len(r), 2)

    def testFixCapacityOnReplace(self):
        r = Route(self.sp, self.earlyC, self.middleC)
        self.assertEqual(r.capacity, self.earlyC.demand + self.middleC.demand)
        r[0] = self.lateC
        self.assertEqual(r.capacity, self.lateC.demand + self.middleC.demand)
        r[1] = self.earlyC
        self.assertEqual(r.capacity, self.lateC.demand + self.earlyC.demand)

class TestRoutes(unittest.TestCase):
    def setUp(self):
        pass


if __name__ == "__main__":
    unittest.main()

