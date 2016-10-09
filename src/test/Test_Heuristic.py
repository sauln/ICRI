import unittest

import src


class Test_Heuristic(unittest.TestCase):
    def setUp(self):
        a = src.Customer(0,src.Point(0,0),0,0,0,0)
        b = src.Customer(1,src.Point(1,1),1,1,1,1)
        c = src.Customer(2,src.Point(2,2),2,2,2,2)        
        cs = [a,b,c]
        sp = src.SolomonProblem("test", 5, 100, cs)
        
        src.Parameters().build(sp)



        dispatch = Dispatch(sp.customers)

    def test_failing(self):
        h = src.Heuristic
        

    # Every heuristic must take a list of customers
    # Then it must take..
        






if __name__ == "__main__":
    unittest.main()

