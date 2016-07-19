import unittest
import pickle

from src.main.Matrices import Matrices
from src.main.SolomonProblem import SolomonProblem

class TestRoute(unittest.TestCase):
    def setUp(self):
        # need to show the entire iteration of the route
        
        
        # all of this logic needs to be encoded in tests 
       
        pass
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


    def testAppendOnlyIfAble(self):
        print("Only append the next node if route is not at maximum capacity")


    def testAppendIncreasesCapacity(self):
        print("When you append to the route, it increments the capacity")

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

