import unittest
import src.prototype.Matricies as mat


class TestMatricies(unittest.TestCase):
    def test_EuclidianDistance(self):
        a = mat.stub(0,0)
        b = mat.stub(0,1)
        d = mat.distance(a,b)
        self.assertEqual(0,0) 




if __name__ == "__main__":
    unittest.main()

