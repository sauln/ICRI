import unittest
import src.prototype.Matrices as mat
import pickle

class stub():
    def __init__(self, x, y):
        self.xcoord = x
        self.ycoord = y

class TestMatrices(unittest.TestCase):
    def setUp(self):
        self.customers = [stub(a,b) for a,b in zip(range(5), range(5))] 
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


if __name__ == "__main__":
    unittest.main()

