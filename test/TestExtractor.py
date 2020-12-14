import unittest
from Fitness import Extractor

class TestExtractor(unittest.TestCase):
    def test_max_height(self):
        self.assertEqual(-1, Extractor.max_height('-------------'))
        self.assertEqual(0, Extractor.max_height('X-------------'))
        self.assertEqual(1, Extractor.max_height('bS------------'))
        self.assertEqual(2, Extractor.max_height('b-Q-----------'))
        self.assertEqual(3, Extractor.max_height('--bbE------E--'))
        self.assertEqual(-1, Extractor.max_height('------E------'))
        self.assertEqual(11, Extractor.max_height('-----------X-'))
        self.assertEqual(11, Extractor.max_height('X----------X-'))

    def test_contains_enemy(self):
        self.assertFalse(Extractor.contains_enemy('--------------'))
        self.assertFalse(Extractor.contains_enemy('X-------------'))
        self.assertTrue(Extractor.contains_enemy('bS-------------'))
        self.assertTrue(Extractor.contains_enemy('b-Q------------'))
        self.assertTrue(Extractor.contains_enemy('--bbE------E---'))
        self.assertTrue(Extractor.contains_enemy('------E--------'))
        self.assertFalse(Extractor.contains_enemy('-----------X--'))

    def test_contains_gap(self):
        self.assertTrue(Extractor.contains_gap('--------------'))
        self.assertTrue(Extractor.contains_gap('------X-------'))
        self.assertTrue(Extractor.contains_gap('--------Xb----'))
        self.assertTrue(Extractor.contains_gap('---xB---------'))
        self.assertTrue(Extractor.contains_gap('-XXXX---------'))
        self.assertFalse(Extractor.contains_gap('X------------'))
        self.assertFalse(Extractor.contains_gap('Q------------'))
        self.assertFalse(Extractor.contains_gap('bB-----------'))
