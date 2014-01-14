"""
    A series of unit tests for the 'word_scrabble' module.

    All tests passed as of version 1.0.
    Author: Nielen Venter
"""

import unittest
from word_scrabblers import WordScrabbleCalculator, WordScrabbleHelper
from word_sets import WordSet, WordSetHelper

class WordScrabbleCalculatorTest(unittest.TestCase):

    def test_when_instantiated_with_non_string(self):
        self.assertRaises(TypeError, WordScrabbleCalculator, 6)

    def test_when_instantiated_with_bad_tiles(self):
        self.assertRaises(TypeError, WordScrabbleCalculator, 'abc6de')
        self.assertRaises(TypeError, WordScrabbleCalculator, 'abc!de')

    def test_when_instantiated_with_too_many_letters(self):
        self.assertRaises(TypeError, WordScrabbleCalculator, 'abcdefgh')
    
    def test_when_instantiated_wth_default_word_set(self):
        default_word_set = WordSet()
        scrabble_calc = WordScrabbleCalculator('')

        self.assertEqual(scrabble_calc.word_set(), default_word_set())

    def test_when_instantiated_wth_custom_word_set(self):
        custom_word_set = WordSet(set(['bat', 'banana', 'shoe', 'dog']))
        scrabble_calc = WordScrabbleCalculator('groade', custom_word_set)

        self.assertEqual(scrabble_calc.word_set(), custom_word_set())

    def test_gets_possible_words(self):
        custom_word_set = WordSet(set(['bat', 'banana', 'shoe', 'dog']))
        scrabble_calc = WordScrabbleCalculator('sdhooeg', custom_word_set)
        possible_words = scrabble_calc.get_possible_words()

        self.assertEqual(set(possible_words), set(['dog', 'shoe']))

    def test_gets_possible_words_with_blank_tile(self):
        custom_word_set = WordSet(set(['bat', 'banana', 'shoe', 'dog']))
        scrabble_calc = WordScrabbleCalculator('sd ooeg', custom_word_set)
        possible_words = scrabble_calc.get_possible_words()

        self.assertEqual(set(possible_words), set(['dog', 'shoe']))

    def test_gets_no_possible_words(self):
        custom_word_set = WordSet(set(['bat', 'banana', 'shoe', 'dog']))
        scrabble_calc = WordScrabbleCalculator('noluck', custom_word_set)
        possible_words = scrabble_calc.get_possible_words()

        self.assertEqual(possible_words, [])

    def test_gets_right_score(self):
        scrabble_calc = WordScrabbleCalculator('', WordSet(set()))
        score = scrabble_calc._get_score('zebra')

        self.assertEqual(score, 10+1+3+1+1)

    def test_gets_right_score_with_blank(self):
        scrabble_calc = WordScrabbleCalculator('ze ra', WordSet(set()))
        score = scrabble_calc._get_score('zebra', scrabble_calc.word)

        self.assertEqual(score, 10+1+0+1+1)

    def test_gets_suggestions_ordered_by_score(self):
        custom_word_set = WordSet(set(['bat', 'banana', 'shoe', 'dog']))
        scrabble_calc = WordScrabbleCalculator('sdhooeg', custom_word_set)
        suggestions = scrabble_calc.get_suggestions(2)

        self.assertEqual(suggestions, ['shoe', 'dog'])

    def test_gets_suggestions_ordered_by_score_with_blank(self):
        custom_word_set = WordSet(set(['bat', 'banana', 'shoe', 'dog']))
        scrabble_calc = WordScrabbleCalculator('sd ooeg', custom_word_set)
        suggestions = scrabble_calc.get_suggestions(2)

        self.assertEqual(suggestions, ['dog', 'shoe'])

    def test_gets_limited_suggestions(self):
        custom_word_set = WordSet(set(['bat', 'banana', 'shoe', 'dog']))
        scrabble_calc = WordScrabbleCalculator('sdhooeg', custom_word_set)
        suggestions = scrabble_calc.get_suggestions(1)

        self.assertEqual(suggestions, ['shoe'])


class WordScrabbleHelperTest(unittest.TestCase):

    def test_when_instantiated_with_word_set(self):
        custom_word_set = WordSet(set(['bat', 'banana', 'shoe', 'dog']))
        scrabble_helper = WordScrabbleHelper('', custom_word_set)

        self.assertEqual(scrabble_helper.word_set(), custom_word_set())

    def test_gets_suggestions_by_adding(self):
        custom_word_set = WordSet(set(['bat', 'banana', 'shoe', 'dog']))
        scrabble_helper = WordScrabbleHelper('sho', custom_word_set)
        suggestion = scrabble_helper.get_alternative_suggestions(1)

        self.assertEqual(suggestion, ['shoe'])

    def test_gets_suggestions_by_substituting(self):
        custom_word_set = WordSet(set(['bat', 'banana', 'shoe', 'dog']))
        scrabble_helper = WordScrabbleHelper('shod', custom_word_set)
        suggestion = scrabble_helper.get_alternative_suggestions(1)

        self.assertEqual(suggestion, ['shoe'])

    def test_gets_suggestions_by_searching(self):
        custom_word_set = WordSet(set(['bat', 'banana', 'shoe', 'dog']))
        scrabble_helper = WordScrabbleHelper('ba', custom_word_set)
        suggestion = scrabble_helper.get_alternative_suggestions(2)

        self.assertEqual(set(suggestion), set(['bat', 'banana']))

    def test_gets_right_suggestion_score(self):
        scrabble_helper = WordScrabbleHelper('zebr', WordSet(set()))
        score = scrabble_helper._get_suggestion_score('zebra')

        self.assertEqual(score, (10+1+3+1+1,))

    def test_gets_right_suggestion_score_range_with_blank(self):
        scrabble_helper = WordScrabbleHelper('ebr ', WordSet(set()))
        score = scrabble_helper._get_suggestion_score('zebra')

        # Low score: player gets 'a'
        # High score: player gets 'z'
        self.assertEqual(score, (0+1+3+1+1, 10+1+3+1+0))

if __name__ == '__main__':
    unittest.main()
