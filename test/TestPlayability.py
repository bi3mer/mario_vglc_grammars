import unittest

from Fitness import playability, expected_playability, percent_playable
from IO.GetLevels import get_super_mario_bros

class TestNGram(unittest.TestCase):
    def test_contrived_playability(self):
        levels = get_super_mario_bros()
        for columns in levels:
            self.assertTrue(playability(columns) < 20)

        columns = []
        columns.append('X------------')
        columns.append('X[[[---------')
        columns.append('X------------')
        columns.append('-------------')

        self.assertEqual(1, playability(columns))
        
        columns[2] = 'X]]]---------'
        self.assertEqual(0, playability(columns))

        columns.append('X---X[[------')
        columns.append('X---X]]------')
        self.assertEqual(0, playability(columns))

    def test_level_playability_with_levels(self):
        for lvl in get_super_mario_bros():
            self.assertEqual(1.0, percent_playable(lvl))

    def test_fail_level_playability(self):
        columns = []
        columns.append('X------------')
        columns.append('X[[[---------')
        columns.append('X------------')
        columns.append('-------------')
        self.assertEqual(1.0, percent_playable(columns))

        columns = []
        columns.append('X------------')
        columns.append('X[[[---------')
        columns.append('X------------')
        columns.append('-------------')
        columns.append('-------------')
        columns.append('-------------')
        columns.append('-------------')
        columns.append('-------------')
        columns.append('-------------')
        columns.append('-------------')
        columns.append('X------------')

        self.assertEqual(9 / len(columns), percent_playable(columns))

        columns = []
        columns.append('X------------')
        columns.append('X[[[---------')
        columns.append('X------------')
        columns.append('X------------')
        columns.append('-------------')
        columns.append('-------------')
        columns.append('-------X-----')
        columns.append('-------X-----')
        columns.append('-------X-----')
        columns.append('-------X-----')
        columns.append('-------------')
        columns.append('X------------')

        self.assertEqual(10 / len(columns), percent_playable(columns))
        
    def test_expected_playability(self):
        heights = [0,0,0,0]
        self.assertEqual(0, expected_playability(heights))

        heights = [0,0,0,3,5,12,5]
        self.assertEqual(1, expected_playability(heights))