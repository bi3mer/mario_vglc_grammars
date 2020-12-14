from math import isclose
import unittest

import Fitness

class TestLeniency(unittest.TestCase):
    def test_leniency(self):
        level = []
        level.append('X---------------')
        level.append('X---------------')
        level.append('X---------------')
        self.assertEqual(0, Fitness.leniency(level))

        level.append('X---------------')
        level.append('XE--------------')
        level.append('X---------------')
        self.assertEqual(0.5, Fitness.leniency(level))

        level.append('X---------------')
        level.append('X---------------')
        level.append('----------------')
        self.assertEqual(1.0, Fitness.leniency(level))

        level.append('X----------------')
        level.append('----XE-----------')
        level.append('X----------------')
        self.assertEqual(2.0, Fitness.leniency(level))

        level.append('X----------------')
        level.append('bBE--------------')
        level.append('X----------------')
        self.assertEqual(2.5, Fitness.leniency(level))
