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
        r = Route(earlyC, lateC)



    def testNotFull(self):
        pass#f = isNotFull(self.sp, r, lateC)
        


    def testTimeAfter(self):
        #isFeasible(sp, route, end)
        r = Route(self.middleC)
        f = isValidTime(self.sp, r, self.lateC)
        self.assertTrue(f, "Later time is valid after an early time")
        
        r = Route(self.lateC)
        f = isValidTime(self.sp, r, self.earlyC)
        self.assertFalse(f, "Early time is not valid after a late time")






if __name__ == "__main__":
    unittest.main()

