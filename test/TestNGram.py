import unittest

from  Grammar import NGram

class TestNGram(unittest.TestCase):
    def test_n_gram_size(self):
        for i in range(2, 20):
            self.assertEqual(i, NGram(i).n)

    def test_n_gram_add_sequence(self):
        ngram = NGram(3)
        ngram.add_sequence("abcd")

        self.assertTrue("a,b" in ngram.grammar)
        self.assertTrue("b,c" in ngram.grammar)

        self.assertEqual(2, len(ngram.grammar.keys()))
        self.assertEqual(1, ngram.grammar["a,b"]["c"])
        self.assertEqual(1, ngram.grammar["b,c"]["d"])

        ngram.add_sequence("abcd")
        self.assertEqual(2, len(ngram.grammar.keys()))
        self.assertEqual(2, ngram.grammar["a,b"]["c"])
        self.assertEqual(2, ngram.grammar["b,c"]["d"])

        ngram.add_sequence("ac")
        self.assertEqual(2, len(ngram.grammar.keys()))
        self.assertEqual(2, ngram.grammar["a,b"]["c"])
        self.assertEqual(2, ngram.grammar["b,c"]["d"])

        ngram.add_sequence("acd")
        self.assertEqual(3, len(ngram.grammar.keys()))
        self.assertEqual(2, ngram.grammar["b,c"]["d"])
        self.assertEqual(2, ngram.grammar["b,c"]["d"])
        self.assertEqual(1, ngram.grammar["a,c"]["d"])

    def test_has_next_step(self):
        gram = NGram(2)
        self.assertFalse(gram.has_next_step("a"))

        gram.add_sequence("ab")
        self.assertTrue(gram.has_next_step("a"))
        self.assertFalse(gram.has_next_step("b"))
        self.assertFalse(gram.has_next_step(""))
        self.assertFalse(gram.has_next_step("a,b"))

    def test_get_output(self):
        gram = NGram(3)
        gram.add_sequence("aab") # aa -> b
        gram.add_sequence("aab") # aa -> b
        gram.add_sequence("aab") # aa -> b
        gram.add_sequence("aab") # aa -> b
        gram.add_sequence("aab") # aa -> b
        gram.add_sequence("aac") # aa -> c
        gram.add_sequence("aac") # aa -> c
        gram.add_sequence("aca") # ac -> a
        gram.add_sequence("acb") # ac -> b

        b_found = 0
        c_found = 0
        for _ in range(100):
            output = gram.get_output("a,a")
            if output == 'b':
                b_found += 1
            elif output == 'c':
                c_found += 1
            else:
                self.fail(f'Unknown output: "{output}"')

        self.assertTrue(b_found > 0)
        self.assertTrue(c_found > 0)
        self.assertTrue(b_found > c_found)

        a_found = 0
        b_found = 0
        for _ in range(100):
            output = gram.get_output("a,c")
            if output == 'a':
                a_found += 1
            elif output == 'b':
                b_found += 1
            else:
                self.fail(f'Unknown output: "{output}"')

        self.assertTrue(a_found > 0)
        self.assertTrue(b_found > 0)

    def test_get_weighted_output(self):
        gram = NGram(4)
        gram.add_sequence("aaac") # aaa -> c
        gram.add_sequence("aaac") # aaa -> c
        gram.add_sequence("aaac") # aaa -> c
        gram.add_sequence("aaac") # aaa -> c
        gram.add_sequence("aaab") # aaa -> b

        gram.add_sequence("bbba") # bbb -> a
        gram.add_sequence("bbba") # bbb -> a
        gram.add_sequence("bbba") # bbb -> a
        gram.add_sequence("bbba") # bbb -> a
        gram.add_sequence("bbbc") # bbb -> c
        gram.add_sequence("bbbc") # bbb -> c
        gram.add_sequence("bbbc") # bbb -> c
        gram.add_sequence("bbbc") # bbb -> c
        gram.add_sequence("bbbc") # bbb -> c
        gram.add_sequence("bbbd") # bbb -> d
        gram.add_sequence("bbbd") # bbb -> d
        gram.add_sequence("bbbd") # bbb -> d
        gram.add_sequence("bbbd") # bbb -> d
        gram.add_sequence("bbbd") # bbb -> d
        gram.add_sequence("bbbd") # bbb -> d

        output = gram.get_weighted_output('a,a,a')
        self.assertEqual(2, len(output))
        self.assertTrue('c' == output[0])
        self.assertTrue('b' == output[1])

        output = gram.get_weighted_output('b,b,b')
        self.assertEqual(3, len(output))
        self.assertTrue('d' == output[0])
        self.assertTrue('c' == output[1])
        self.assertTrue('a' == output[2])