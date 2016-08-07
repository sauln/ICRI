import unittest


from src.main.Algorithms.Heuristic import Heuristic
from src.main.BaseObjects.Customer import Customer
from src.main.BaseObjects.SolomonProblem import SolomonProblem
from src.main.BaseObjects.Parameters import Parameters

class TestHeuristic(unittest.TestCase):
    def setUp(self):
        self.depot   = Customer(0, 0, 0, 20, 0, 200, 0)
        self.lateC   = Customer(1, 5, 5, 20, 99, 200, 4)
        self.middleC = Customer(2, 10,10, 20, 45,55, 9)
        self.a       = Customer(3, 1,  10, 20,  0,  20, 3)
        self.b       = Customer(4, 2,   5, 20, 99, 200, 4)
        self.c       = Customer(5, 30, 10, 20, 45,  55, 9)
        self.d       = Customer(6, 6,  10, 20,  30,  40, 3)
        self.e       = Customer(7, 10,  5, 20, 99, 200, 4)
        self.f       = Customer(8, 25, 10, 20, 45,  55, 9)
        self.g       = Customer(9, 10,  5, 20, 99, 200, 4)
        self.h       = Customer(10, 25, 10, 20, 45,  55, 9)

        customers = [self.depot, self.lateC, self.middleC, 
                     self.a, self.b, self.c, self.d, 
                     self.e, self.f, self.g, self.h]
        
        self.customers = list(customers)
        self.customers.remove(self.depot)
        
        sp = SolomonProblem("test", 7, 100, customers)       
       
        parameters = Parameters()
        parameters.build(sp, 10,10)

    def testRunIsRightSize(self):
        heur = Heuristic()      
        solution = heur.run([1]*7, self.depot, self.customers, self.depot)
        self.assertLessEqual(len(solution), 7)
        


if __name__ == "__main__":
    unittest.main()
