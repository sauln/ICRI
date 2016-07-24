import unittest
import pickle
import copy

from src.main.Matrices import Matrices
from src.main.SolomonProblem import SolomonProblem
from src.main.Customer import Customer

class TestSolomonProblem(unittest.TestCase):
    def setUp(self):
        pass

    def test_Eq(self):
        s = SolomonProblem("test1", 4,4,4)
        r = SolomonProblem("test1", 4,4,4)
        self.assertEqual(s, r)

        t = SolomonProblem("test3", 4,4,5)
        self.assertNotEqual(s, t)
       
        q = SolomonProblem("test4", 1,2,3)
        self.assertNotEqual(s,q)
        self.assertEqual(s,copy.copy(s))
        self.assertEqual(r,r)



class TestCustomer(unittest.TestCase):
    def setUp(self):
        pass

    def test_Eq(self):

        nargs = 7
        args = [1]*7
        c = Customer(*args)
        d = Customer(*args)
        self.assertEqual(c,d)

        for i in range(nargs):
            args = [1]*nargs
            args[i] = 9
            d = Customer(*args)
            self.assertNotEqual(c,d)

if __name__ == "__main__":
    unittest.main()

