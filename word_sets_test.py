"""
    A series of unit tests for the 'word_set' module.

    Latest version for which all tests passed: 1.0.
    Author: Nielen Venter
"""

import unittest
from word_sets import WordSet, WordSetHelper

class WordSetTest(unittest.TestCase):

    def test_when_instantiated_with_custom_set(self):
        collection_of_words = set(['bat', 'banana', 'shoe', 'dog'])
        word_set = WordSet(collection_of_words)

        self.assertEqual(word_set(), collection_of_words)

    def test_when_instantiated_with_empty_set(self):
        collection_of_words = set()
        word_set = WordSet(collection_of_words)

        self.assertEqual(word_set(), collection_of_words)

    def test_when_instantiated_with_bad_arguments_1(self):
        self.assertRaises(TypeError, WordSet, 'banana')

    def test_when_instantiated_with_bad_arguments_2(self):
        collection_of_words = set(['banana', 6])
        self.assertRaises(TypeError, WordSet, collection_of_words)

    def test_set_is_loaded_when_instantiated_with_default(self):
        word_set = WordSet()
        self.assertIsInstance(word_set(), set)

    def test_word_found_in_set(self):
        collection_of_words = set(['bat', 'banana', 'shoe', 'dog'])
        word_set = WordSet(collection_of_words)

        self.assertEqual(word_set['banana'], True)

    def test_word_not_found_in_set(self):
        collection_of_words = set(['bat', 'banana', 'shoe', 'dog'])
        word_set = WordSet(collection_of_words)

        self.assertEqual(word_set['apple'], False)

class WordSetTestHelper(unittest.TestCase):

    def test_when_instantiated_with_word_set(self):
        word_set = WordSet()
        word_set_helper = WordSetHelper(word_set)

        self.assertIsInstance(word_set_helper(), set)

    def test_correction_by_adding(self):
        collection_of_words = set(['bat', 'banana', 'shoe', 'dog'])
        word_set_helper = WordSetHelper(collection_of_words)
        correction = word_set_helper._find_words_by_adding('do')

        self.assertEqual(correction, ['dog'])

    def test_correction_by_substituting(self):
        collection_of_words = set(['bat', 'banana', 'shoe', 'dog'])
        word_set_helper = WordSetHelper(collection_of_words)
        correction = word_set_helper._find_words_by_substituting('dag')

        self.assertEqual(correction, ['dog'])

    def test_correction_by_removing(self):
        collection_of_words = set(['bat', 'banana', 'shoe', 'dog'])
        word_set_helper = WordSetHelper(collection_of_words)
        correction = word_set_helper._find_words_by_removing('doag')
        self.assertEqual(correction, ['dog'])

    def test_correction_by_swapping(self):
        collection_of_words = set(['bat', 'banana', 'shoe', 'dog'])
        word_set_helper = WordSetHelper(collection_of_words)
        correction = word_set_helper._find_words_by_swapping('dgo')

        self.assertEqual(correction, ['dog'])

    def test_correction_by_removing(self):
        collection_of_words = set(['bat', 'banana', 'shoe', 'dog'])
        word_set_helper = WordSetHelper(collection_of_words)
        correction = word_set_helper._find_words_by_removing('doag')
        self.assertEqual(correction, ['dog'])

    def test_correction_by_substituting(self):
        collection_of_words = set(['bat', 'banana', 'shoe', 'dog'])
        word_set_helper = WordSetHelper(collection_of_words)
        correction = word_set_helper._find_words_by_substituting('dag')

        self.assertEqual(correction, ['dog'])

    def test_correction_by_searching(self):
        collection_of_words = set(['bat', 'banana', 'shoe', 'dog'])
        word_set_helper = WordSetHelper(collection_of_words)
        correction = word_set_helper._find_closest_words_by_searching('ban')

        self.assertEqual(correction, ['banana'])

    def test_get_alternative_words(self):
        collection_of_words = set(['bat', 'banana', 'shoe', 'dog'])
        word_set_helper = WordSetHelper(collection_of_words)
        correction = word_set_helper.get_alternative_words('ban')

        self.assertEqual(correction, ['bat', 'banana'])

    def test_get_alternative_words_limited(self):
        collection_of_words = set(['bat', 'banana', 'shoe', 'dog'])
        word_set_helper = WordSetHelper(collection_of_words)
        correction = word_set_helper.get_alternative_words('ban', 1)

        self.assertEqual(correction, ['bat'])


if __name__ == "__main__":
    unittest.main()
