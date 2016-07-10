import unittest
import pickle

import src.model.Matrices as mat

class stub():
    def __init__(self, x, y):
        self.xcoord = x
        self.ycoord = y

    def __str__(self):
        return "Stub ({},{})".format(self.xcoord, self.ycoord)
    
    def __repr__(self):
        return self.__str__()


class TestMatrices(unittest.TestCase):
    def setUp(self):
        self.customers = [stub(a,b) for a,b in zip(range(5), range(5))] 
        self.problem = mat.SolomonProblem("test", 5,5, self.customers) 
        self.m = mat.Matrices(self.customers)

    def test_DistEuclid(self):
        a = stub(0,0)
        b = stub(0,1)
        d = mat.Matrices(self.customers).distEuclid(a,b)
        self.assertEqual(0,0) 
        
    def test_matrixiscorrectsize(self):
        self.assertEqual(self.m.distMatrix.shape, (5,5))

    def test_diagonal_is_zeros(self):
        for i in range(5):
            self.assertEqual(self.m.distMatrix[i,i], 0)

    def test_timeanddistMatricesSameSize(self):
        self.assertEqual(self.m.distMatrix.shape, self.m.timeMatrix.shape)

    def test_buildmatricesfromfile(self):
        filename="tmp.p"
        with open(filename, "wb") as f:
            pickle.dump(self.problem, f)
        
        m = mat.buildMatricesFromCustomerFile(filename)

        self.assertEqual(m, self.m)

    def test_Eq(self):
        m2 = mat.Matrices(self.customers)
        self.assertEqual(self.m, m2)

        c2 = list( self.customers )
        c2.append(stub(99,99))
        self.assertEqual(len(c2), len(self.customers)+1)
        
        m_diff = mat.Matrices(c2)
        self.assertNotEqual(self.m, m_diff)

if __name__ == "__main__":
    unittest.main()

