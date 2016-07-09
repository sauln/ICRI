import unittest
import src.prototype.Matricies as mat
import pickle

class TestMatricies(unittest.TestCase):
    def test_DistEuclid(self):
        a = mat.stub(0,0)
        b = mat.stub(0,1)
        d = mat.distEuclid(a,b)
        self.assertEqual(0,0) 
        

    def test_matrixiscorrectsize(self):
        customers = [mat.stub(a,b) for a,b in zip(range(5), range(5))] 
        a = mat.distanceMatrix(customers)
        self.assertEqual(a.shape, (5,5))

    def test_diagonal_is_zeros(self):
        customers = [mat.stub(a,b) for a,b in zip(range(5), range(5))]
        a = mat.distanceMatrix(customers)

        for i in range(5):
            self.assertEqual(a[i,i], 0)


if __name__ == "__main__":
    unittest.main()

