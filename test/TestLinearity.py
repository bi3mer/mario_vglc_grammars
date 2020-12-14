from math import isclose
import unittest

import Fitness

class TestLinearity(unittest.TestCase):
    def test_linearity(self):
        level = []
        level.append('X---------------')
        level.append('X---------------')
        level.append('X---------------')
        self.assertEqual(0, Fitness.linearity(level))

        level.append('X---------------')
        level.append('XE--------------')
        level.append('X---------------')
        self.assertEqual(0, Fitness.linearity(level))

        level = []
        level.append('B------')
        level.append('-S-----')
        level.append('XXX----')
        level.append('-------')
        level.append(']]]>E--')
        level.append('[[[>X--')
        level.append('-----Q-')
        level.append('------]')
        level.append('-------')
        self.assertEqual(0, Fitness.linearity(level))

        level.append('-------')
        level.append('--QE---')
        self.assertNotEqual(0, Fitness.linearity(level))

    def test_max_linearity(self):
        self.assertEqual(8 * 10 + 7 * 10, Fitness.max_linearity(20, 16))