import unittest

from src.main.Customer import Customer

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

