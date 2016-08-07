import unittest
import pickle
import copy

from src.main.BaseObjects.SolomonProblem import SolomonProblem

class TestSolomonProblem(unittest.TestCase):
    def setUp(self):
        pass

    def testEq(self):
        s = SolomonProblem("test1", 4,4,4)
        r = SolomonProblem("test1", 4,4,4)
        self.assertEqual(s, r)

        t = SolomonProblem("test3", 4,4,5)
        self.assertNotEqual(s, t)
       
        q = SolomonProblem("test4", 1,2,3)
        self.assertNotEqual(s,q)
        self.assertEqual(s,copy.copy(s))
        self.assertEqual(r,r)

if __name__ == "__main__":
    unittest.main()

