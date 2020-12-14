from math import isclose

import unittest
from Grammar import BackoffNGram

class TestBackoffNGram(unittest.TestCase):
    def test_n_gram_size(self):
        self.assertEqual(1, BackoffNGram(1, [1]). n)
        self.assertEqual(2, BackoffNGram(2, [1, 0]). n)
        self.assertEqual(3, BackoffNGram(3, [1, 0, 0]). n)
        self.assertEqual(4, BackoffNGram(4, [1, 0, 0, 0]). n)
        self.assertEqual(5, BackoffNGram(5, [1, 0, 0, 0, 0]). n)

        with self.assertRaises(AssertionError):
            BackoffNGram(3, [1, 0, 0, 0, 0])

        with self.assertRaises(AssertionError):
            BackoffNGram(3, [1, 2, 0])

    def test_n_gram_add_sequence(self):
        gram = BackoffNGram(4, [0.8, 0.1, 0.05, 0.05])
        gram.add_sequence("abcd")
        self.assertEqual(6, len(gram.grammar))
        self.assertEqual(4, len(gram.unigram.counts))

        # test 4-gram
        self.assertTrue("a,b,c" in gram.grammar)
        self.assertEqual(1, len(gram.grammar["a,b,c"]))
        self.assertEqual(1, gram.grammar["a,b,c"]["d"])

        # test tri-gram
        self.assertTrue("a,b" in gram.grammar)
        self.assertEqual(1, len(gram.grammar["a,b"]))
        self.assertEqual(1, gram.grammar["a,b"]["c"])
        
        self.assertTrue("b,c" in gram.grammar)
        self.assertEqual(1, len(gram.grammar["b,c"]))
        self.assertEqual(1, gram.grammar["b,c"]["d"])

        # test bi-gram
        self.assertTrue("a" in gram.grammar)
        self.assertTrue("b" in gram.grammar["a"])
        self.assertEqual(1, gram.grammar["a"]["b"])

        self.assertTrue("b" in gram.grammar)
        self.assertTrue("c" in gram.grammar["b"])
        self.assertEqual(1, gram.grammar["b"]["c"])

        self.assertTrue("c" in gram.grammar)
        self.assertTrue("d" in gram.grammar["c"])
        self.assertEqual(1, gram.grammar["c"]["d"])
        
        # test uni-gram
        self.assertEqual(1, gram.unigram.counts["a"])
        self.assertEqual(1, gram.unigram.counts["b"])
        self.assertEqual(1, gram.unigram.counts["c"])
        self.assertEqual(1, gram.unigram.counts["d"])

    def test_has_next_step(self):
        gram = BackoffNGram(2, [0.6, 0.4])
        self.assertFalse(gram.has_next_step("a"))

        gram.add_sequence("ab")
        self.assertTrue(gram.has_next_step("a"))
        self.assertTrue(gram.has_next_step("b"))
        self.assertTrue(gram.has_next_step(""))
        self.assertTrue(gram.has_next_step("ab"))

    def test_get_output(self):
        gram = BackoffNGram(3, [0.1, 0.2, 0.7])
        gram.add_sequence("aab") # aa -> b, a -> a, a -> b, a, a, b
        gram.add_sequence("aab") # aa -> b, a -> a, a -> b, a, a, b
        gram.add_sequence("aab") # aa -> b, a -> a, a -> b, a, a, b
        gram.add_sequence("aab") # aa -> b, a -> a, a -> b, a, a, b
        gram.add_sequence("aab") # aa -> b, a -> a, a -> b, a, a, b
        gram.add_sequence("aac") # aa -> c, a -> a, a -> c, a, a, c
        gram.add_sequence("aac") # aa -> c, a -> a, a -> c, a, a, c
        gram.add_sequence("aca") # ac -> a, a -> c, a -> a, a, c, a
        gram.add_sequence("acb") # ac -> b, a -> c, c -> b, a, c, b

        counts = { 'a': 0, 'b': 0, 'c': 0}
        for _ in range(100):
            counts[gram.get_output("a,a")] += 1

        self.assertTrue(counts['a'] == 0)
        self.assertTrue(counts['b'] > 0)
        self.assertTrue(counts['c'] > 0)

        counts = { 'a': 0, 'b': 0, 'c': 0}
        for _ in range(100):
            counts[gram.get_output("a,d")] += 1
    
        self.assertTrue(counts['a'] > 0)
        self.assertTrue(counts['b'] > 0)
        self.assertTrue(counts['c'] > 0)

    def test_get_probability(self):
        gram = BackoffNGram(4, [0.05, 0.05, 0.2, 0.7])
        self.assertEqual(0, gram.get_probability(['a', 'a'], 'b'))
        self.assertEqual(0, gram.get_probability(['a'], 'b'))
        self.assertEqual(0, gram.get_probability(['a'], 'b'))

        gram.add_sequence('aaab')
        # a -> 3/4
        # b -> 1/4
        self.assertEqual(0.05 * 0.75, gram.get_probability([], 'a'))
        self.assertEqual(0.05 * 0.25, gram.get_probability([], 'b'))

        # aa -> 2/3
        # ab -> 1/3
        self.assertEqual(0.05 * (2/3), gram.get_probability(['a'], 'a'))
        self.assertEqual(0.05 * (1/3), gram.get_probability(['a'], 'b'))

        # aaa -> 1/2
        # aab -> 1/2
        self.assertEqual(0.2 * 0.5, gram.get_probability(['a', 'a'], 'a'))
        self.assertEqual(0.2 * 0.5, gram.get_probability(['a', 'a'], 'b'))

        # aaab -> 1/1
        self.assertEqual(0.7, gram.get_probability(['a', 'a', 'a'], 'b'))
        self.assertEqual(0.05 * (1/3), gram.get_probability(['c', 'd', 'a'], 'b'))
        self.assertEqual(0.05 * 0.75, gram.get_probability(['c', 'd', 'z'], 'a'))

    def test_sequence_probability(self):
        gram = BackoffNGram(4, [0.05, 0.05, 0.2, 0.7])
        self.assertEqual(0, gram.sequence_probability('a,a,b'))

        gram.add_sequence('aaab')
        self.assertTrue(
            isclose(
                (0.05 * 0.75) * (0.05 * (2/3)) * (0.2 * 0.5) * 0.7, 
                gram.sequence_probability(['a','a','a','b'])))