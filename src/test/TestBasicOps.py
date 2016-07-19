import unittest
import pickle

from src.main.basicOps import *
from src.main.Routes import Routes, Route

from src.main.SolomonProblem import SolomonProblem, Customer


# test H_gamma
# assert that it works exactly how it should
# it should start a new route - when the best next is infeasible
# it should use all of the customers and no more
# 





class TestIsFeasible(unittest.TestCase):
    def setUp(self):
        self.sp = SolomonProblem("test", 5, 100, None)
        
        earlyC = Customer(0, 0, 0, 20, 0, 10, 3)
        lateC = Customer(1, 5, 5, 20, 99, 200, 4)
        middleC = Customer(2, 10,10, 20, 45,55, 9)

        self.earlyC, self.lateC, self.middleC = earlyC, lateC, middleC 
        
        self.sp.customers = [earlyC, lateC, middleC]
        self.sp.prepare()
        r = Route(self.sp, earlyC, lateC)

    def testNotFull(self):
        r = Route(self.sp, self.middleC)
        
        t = isNotFull(self.sp, r, self.lateC)
        self.assertTrue(t, "There is plenty of room left")

        self.sp.capacity = 25
        f = isNotFull(self.sp, r, self.lateC)
        self.assertFalse(f, "There is not enough room left")

    def testTimeAfter(self):
        #isFeasible(sp, route, end)
        r = Route(self.sp, self.middleC)
        f = isValidTime(self.sp, r, self.lateC)
        self.assertTrue(f, "Later time is valid after an early time")
        
        r = Route(self.sp, self.lateC)
        f = isValidTime(self.sp, r, self.earlyC)
        self.assertFalse(f, "Early time is not valid after a late time")

if __name__ == "__main__":
    unittest.main()

