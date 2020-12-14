from math import isclose
import unittest

from Fitness import Linearity

class TestExtractor(unittest.TestCase):
    def test_get_slope_and_intercept(self):
        # using example from web: https://www.mathsisfun.com/data/least-squares-regression.html
        x = [2, 3, 5, 7, 9]
        y = [4, 5, 7, 10, 15]

        m, b = Linearity.get_slope_and_intercept(x, y)
        self.assertTrue(isclose(m, 1.518, abs_tol=1e-3))
        self.assertTrue(isclose(b, 0.305, abs_tol=1e-3))