import unittest
import pickle

from src.main.basicOps import *
from src.main.Routes import Routes, Route
from src.main.SolomonProblem import SolomonProblem, Customer

class TestCostFunctions(unittest.TestCase):
    def setUp(self):
        self.sp = SolomonProblem("test", 5, 100, None)
        
        earlyC  = Customer(0, 0, 0, 20, 0, 10, 3)
        lateC   = Customer(1, 5, 5, 20, 99, 200, 4)
        middleC = Customer(2, 10,10, 20, 45,55, 9)
        a = Customer(3, 1,  10, 20,  0,  10, 3)
        b = Customer(4, 2,   5, 20, 99, 200, 4)
        c = Customer(5, 30, 10, 20, 45,  55, 9)
        d = Customer(6, 6,  10, 20,  0,  10, 3)
        e = Customer(7, 10,  5, 20, 99, 200, 4)
        f = Customer(8, 25, 10, 20, 45,  55, 9)
        g = Customer(9, 10,  5, 20, 99, 200, 4)
        h = Customer(10, 25, 10, 20, 45,  55, 9)

        self.sp.customers = [earlyC, lateC, middleC, a, b, c, d, e, f, g, h]

        self.earlyC, self.lateC, self.middleC = earlyC, lateC, middleC 
        self.a, self.b, self.c, self.d, self.e = a,b,c,d,e
        self.f, self.g, self.h = f,g,h

        self.sp.prepare()
        self.delta = [1]*7

        self.routes = Routes(self.sp, earlyC)

    def testHeuristicIsPositive(self):
        r = Route(self.sp, self.earlyC)
        
        for cust in self.sp.customers:
            _, _, c = heuristic(self.sp, self.delta, r, cust, self.lateC)
            self.assertGreaterEqual(c, 0) 

class TestGetNodes(unittest.TestCase):
    def setUp(self):
        self.sp = SolomonProblem("test", 5, 100, None)
        
        earlyC  = Customer(0, 0, 0, 20, 0, 10, 3)
        lateC   = Customer(1, 5, 5, 20, 99, 200, 4)
        middleC = Customer(2, 10,10, 20, 45,55, 9)

        a = Customer(3, 1,  10, 20,  0,  10, 3)
        b = Customer(4, 2,   5, 20, 99, 200, 4)
        c = Customer(5, 30, 10, 20, 45,  55, 9)
        d = Customer(6, 6,  10, 20,  0,  10, 3)
        e = Customer(7, 10,  5, 20, 99, 200, 4)
        f = Customer(8, 25, 10, 20, 45,  55, 9)
        g = Customer(9, 10,  5, 20, 99, 200, 4)
        h = Customer(10, 25, 10, 20, 45,  55, 9)

        self.sp.customers = [earlyC, lateC, middleC, a, b, c, d, e, f, g, h]

        self.earlyC, self.lateC, self.middleC = earlyC, lateC, middleC 
        self.a, self.b, self.c, self.d, self.e = a,b,c,d,e
        self.f, self.g, self.h = f,g,h

        self.sp.prepare()
        self.delta = [1]*7

        self.routes = Routes(self.sp, earlyC)

    def testNextNodesAreFeasible(self):
        nextNodes = getBestNNodes(self.sp, self.delta, self.routes, \
            self.sp.customers, self.middleC, 5)
        for r, _, e, _ in nextNodes:
            self.assertTrue(isFeasible(self.sp, r, e))

    def testNextNodesAreAscendingOrder(self):
        nextNodes = getBestNNodes(self.sp, self.delta, self.routes, \
            self.sp.customers, self.middleC, 5)

        for i in range(len(nextNodes) - 1):
            rl, sl, el, cl = nextNodes[i]
            rr, sr, er, cr = nextNodes[i+1]
            self.assertLessEqual(cl, cr)
    
    def testTopNodeIsMaxOfNNodes(self):
        nextNodes = getBestNNodes(self.sp, self.delta, self.routes, \
            self.sp.customers, self.middleC, 5)

        nt = min(nextNodes, key = lambda x: x[3])
        top = getBestNode(self.sp, self.delta, self.routes, \
            self.sp.customers, self.middleC)

        self.assertEqual(top, nt)

    def testNNodesIsRightSize(self):
        nextNodes = getBestNNodes(self.sp, self.delta, self.routes, \
            self.sp.customers, self.middleC, 5)

        self.assertEqual(len(nextNodes), 5)

        nextNodes = getBestNNodes(self.sp, self.delta, self.routes, \
            self.sp.customers, self.middleC, 1)

        self.assertEqual(len(nextNodes), 1)

        nextNodes = getBestNNodes(self.sp, self.delta, self.routes, \
            self.sp.customers, self.middleC, 99)

        self.assertEqual(len(nextNodes), len(self.sp.customers))


class TestIsFeasible(unittest.TestCase):
    def setUp(self):
        self.sp = SolomonProblem("test", 5, 100, None)
        
        earlyC  = Customer(0, 0, 0, 20, 0, 10, 3)
        lateC   = Customer(1, 5, 5, 20, 99, 200, 4)
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
        r = Route(self.sp, self.middleC)
        t = isValidTime(self.sp, r, self.lateC)
        self.assertTrue(t, "Later time is valid after an early time")
        
        r = Route(self.sp, self.lateC)
        f = isValidTime(self.sp, r, self.earlyC)
        self.assertFalse(f, "Early time is not valid after a late time")

    def testIsFeasible(self):
        r = Route(self.sp, self.middleC) 
        t = isFeasible(self.sp, r, self.lateC)
        self.assertTrue(t)
        f = isFeasible(self.sp, r, self.earlyC)
        self.assertFalse(f)


if __name__ == "__main__":
    unittest.main()

