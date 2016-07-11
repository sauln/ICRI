import unittest
import pickle
import src.model.Matrices as mat
import src.model.SolomonProblem as sp
import copy
# There is very little to test here.

class TestSolomonProblem(unittest.TestCase):
    def setUp(self):
        pass

    def test_Eq(self):
        s = sp.SolomonProblem("test1", 4,4,4)
        r = sp.SolomonProblem("test1", 4,4,4)
        self.assertEqual(s, r)

        t = sp.SolomonProblem("test3", 4,4,5)
        self.assertNotEqual(s, t)
       
        q = sp.SolomonProblem("test4", 1,2,3)
        self.assertNotEqual(s,q)
        self.assertEqual(s,copy.copy(s))
        self.assertEqual(r,r)



class TestCustomer(unittest.TestCase):
    def setUp(self):
        pass

    def test_Eq(self):

        nargs = 7
        args = [1]*7
        c = sp.Customer(*args)
        d = sp.Customer(*args)
        self.assertEqual(c,d)

        for i in range(nargs):
            args = [1]*nargs
            args[i] = 9
            d = sp.Customer(*args)
            self.assertNotEqual(c,d)

if __name__ == "__main__":
    unittest.main()

