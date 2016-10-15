import unittest
from random import randint
import numpy as np

from src import Cost, Vehicle, Customer, Point
import Stub

class TestCost(unittest.TestCase):
    def setUp(self):
        self.depot = Customer(0, Point(0,0), 20, 0, 200, 0)
        self.vehicle = Vehicle(self.depot, 100)

    def test_cost_of_vehicles(self):
        vehicles = [Stub.Vehicle(10), Stub.Vehicle(15), Stub.Vehicle(20)]
        cost = Cost.of_vehicles(vehicles)
        self.assertEqual(cost, (3, 45))
    
    def test_euclid_d(self):
        a = Point(0,0)
        b = Point(1,1)
        self.assertEqual(Cost.euclidean_cust(a,a), 0)
        self.assertEqual(Cost.euclidean_cust(a,b), np.sqrt(2)) 

    def test_gnnh_ge0(self):
        for i in range(100):
            x,y = randint(-100, 100), randint(-100, 100)
            rt = randint(50, 200)
            cust = Customer(0, Point(x,y), 10, rt, rt+randint(0,25), 10)
            c = Cost.gnnh([1]*5, self.vehicle, cust)
            self.assertGreaterEqual(c, 0)

    def test_farther_cost_more(self):
        cust1 = Customer(0, Point(10,10), 10, 75, 100, 10)
        cust2 = Customer(0, Point(20,20), 10, 75, 100, 10)
      
        c1 = Cost.gnnh([1,0.9,0.8,0.7,0.6], self.vehicle, cust1)
        c2 = Cost.gnnh([1,0.9,0.8,0.7,0.6], self.vehicle, cust2)
        self.assertGreater(c2, c1)

if __name__ == "__main__":
    unittest.main()

