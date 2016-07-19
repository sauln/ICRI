import unittest
import pickle

from src.main.SolomonProblem import SolomonProblem, Customer
from src.main.Routes import Route, Routes

class TestRoute(unittest.TestCase):
    def setUp(self):
        
        # all of this logic needs to be encoded in tests 
        '''
        preface = "Number of stops: {}\nCapcity: {}".format(len(self.r), self.capacity)

        route = ""
        total = 0
        for c in self.r:
            route += "\n custNo {}=>arrival time:{}\n\t service len:{}\n\t demand: {}"\
                .format(c.custNo, c._arrivalTime, c.serviceLen, c.demand)
            total += c.demand
            route += "\t\tCurrent capcity: {}".format(total)


        return "Detailed description of route:" + preface + route
        '''
        self.sp = SolomonProblem("test", 5, 100, None)
        
        earlyC = Customer(0, 0, 0, 20, 0, 10, 3)
        lateC = Customer(1, 5, 5, 20, 99, 200, 4)
        middleC = Customer(2, 10,10, 20, 45,55, 9)

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

    def testRemoveDecrementsCapacity(self):
        print("I don't think I ever remove, but if so, it should decrement the capacity count")

    def testConstructorAddsAllElements(self):
        print("The constructor is atypical. It should behave as intended")

    def testSetItem(self):
        print("I think the logic in __setitem__ has been supplanted by the append method")


class TestRoutes(unittest.TestCase):
    def setUp(self):
        pass


if __name__ == "__main__":
    unittest.main()

