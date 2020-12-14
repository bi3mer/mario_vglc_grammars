import unittest
import NGram

class TestUniGram(unittest.TestCase):
    def test_unigram_add_sequence(self):
        unigram = NGram.build(1)
        unigram.add_sequence("abcdef")

        for token in unigram.counts:
            self.assertEqual(unigram.counts[token], 1)

        unigram.add_sequence("abcdef")
        for token in unigram.counts:
            self.assertEqual(unigram.counts[token], 2)

        unigram.add_sequence("g")
        self.assertEqual(unigram.counts["g"], 1)

        unigram = NGram.build(1)

        unigram.add_sequence("ab")
        counts = { "a": 1, "b": 1}
        for key in unigram.counts:
            self.assertEqual(counts[key], unigram.counts[key])

        unigram.add_sequence("abcd")
        counts["a"] = 2
        counts["b"] = 2
        counts["c"] = 1
        counts["d"] = 1
        for key in unigram.counts:
            self.assertEqual(counts[key], unigram.counts[key])

    def test_get_probability(self):
        unigram = NGram.build(1)

        unigram.add_sequence("ab")
        self.assertEqual(0.5, unigram.get_probability("a"))
        self.assertEqual(0.5, unigram.get_probability("b"))
        self.assertEqual(0.0, unigram.get_probability("c"))

        unigram.add_sequence("bb")
        self.assertEqual(0.25, unigram.get_probability("a"))
        self.assertEqual(0.75, unigram.get_probability("b"))
        self.assertEqual(0.0, unigram.get_probability("c"))
        self.assertEqual(0.0, unigram.get_probability("d"))

    def test_has_next_step(self):
        unigram = NGram.build(1)
        self.assertFalse(unigram.has_next_step())

        unigram.add_sequence("aa")
        self.assertTrue(unigram.has_next_step())

    def test_get_output(self):
        unigram = NGram.build(1)
        unigram.add_sequence("aaababcd")

        a_found = 0
        b_found = 0
        c_found = 0
        d_found = 0

        for _ in range(1000):
            received = unigram.get_output()
            if received == 'a':
                a_found += 1
            elif received == 'b':
                b_found += 1
            elif received == 'c':
                c_found += 1
            elif received == 'd':
                d_found += 1
            else:
                self.fail(f'Should not have been able to receive "{received}"')
        
        self.assertTrue(a_found > 0)
        self.assertTrue(b_found > 0)
        self.assertTrue(c_found > 0)
        self.assertTrue(d_found > 0)
        self.assertTrue(a_found > d_found)  

    def test_get_weighted_output(self):
        unigram = NGram.build(1)
        unigram.add_sequence("aaababcd")

        output = unigram.get_weighted_output()
        self.assertEqual(4, len(output))
        self.assertTrue('a' in output)
        self.assertTrue('b' in output)
        self.assertTrue('c' in output)
        self.assertTrue('d' in output)

        alternate_found = False
        for _ in range(5):
            new_output = unigram.get_weighted_output()
            if output != new_output:
                alternate_found = True

        self.assertTrue(alternate_found)
            