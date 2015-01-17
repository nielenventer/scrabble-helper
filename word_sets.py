"""
    This module contains two classes: WordSet and WordSetHelper.

    WordSet loads a set of words from a text file, and can be used to check 
    if a given word is contained in that set.
    The file should be placed in the same directory as this module; 
    the default name is 'words.txt'.
    The shorthand word_set[word] will return True or False if the word 
    is in the set or not.

    WordSetHelper is an extension of WordSet, which can give alternative
    suggestions to a given word, based on the words in the set.
    It finds suggestions using small changes in the given word, such
    as systematically adding, substituting, removing and swapping letters.
    It can also search through the set to find the closest matches (alphabetically).
    The 'get_alternative_words' method searches using the search order defined in
    'search_order' attribute. 

    Profiling (using iPython) revealed no significant bottlenecks.

    Requires Python 2.7.*, not compatible with Python 3.

    Version: 1.0
    Author: Nielen Venter
"""

import os
import re

class WordSet(object):
    """
        An unordered collection of words (in the form of strings).
        Can be used as a spelling checker.
    """
    def __init__(self, word_set=None):
        if word_set is not None:
            # If a word set is passed in, make sure it is a set,
            # and all it's elements are strings.
            word_set_type_ok = isinstance(word_set, set) and \
                                    all(isinstance(word, str) for word in word_set)
            if not word_set_type_ok:
                raise TypeError
            self.word_set = word_set  
        else:
            # If no word set was passed in, load one.
            self.load_word_set()

    def __call__(self):
        return self.word_set

    def __repr__(self):
        return "A set of %d words." % (len(self.word_set))

    def __getitem__(self, word):
        """ 
            The get item method is used as a short-hand for checking
            whether the word set contains a given word.
        """
        try:
            return word.lower() in self.word_set
        except AttributeError:
            return False

    def load_word_set(self, file_name="words.txt"):
        """
            Loads the given file name, and converts it to a set.
            Defaults to words.txt, a text file containing a large
            collection of English words.
        """
        file_path = self._find_word_set_path(file_name)

        # Remove leading and trailing whitespace from the words, and seperate them by line.
        self.word_set = set(self._load_text_from_file(file_path).strip(' ').split('\n'))
    
    def _find_word_set_path(self, file_name):
        """
            Gets the path of the word file, assuming it's in the same directory as this script.
        """
        return os.path.split(os.path.abspath(__file__))[0] + os.sep + file_name

    def _load_text_from_file(self, file_path):
        """
            Loads and returns the text from a given file path.
        """
        try:
            return open(file_path, 'r').read()
        except IOError:
            print "Warning: File name not found."
            print "No text loaded."
            return str()

class WordSetHelper(WordSet):
    """ 
        Class for providing valid alternatives to
        a given word. Can be used as a spelling correcter.
    """
    def __init__(self, word_set=None):
        # Allow a WordSet object to be passed in (in case of upgrade)
        if type(word_set) is WordSet:
            self.word_set = word_set()
        else:
            super(WordSetHelper, self).__init__(word_set)

        # Priority order of searching, quickest and most likely go first.
        self.search_order = [self._find_words_by_swapping, 
                                self._find_words_by_removing,
                                self._find_words_by_adding,
                                self._find_words_by_substituting,
                                self._find_closest_words_by_searching]

    def get_alternative_words(self, input_word, number_of_words=None):
        """ 
            Get the 'n' closest alternative words, where the 
            closeness is determined by the search method used to get it.
        """
        number_of_alternatives = (number_of_words or len(self.word_set))

        alternatives = []
        for search in self.search_order:
            for word in search(input_word):
                # Return only unique alternatives.
                word_is_unique = word not in alternatives and \
                                    word != input_word
                if word_is_unique:
                    alternatives.append(word)

                # Stop searching if the requested number of words was reached.
                if len(alternatives) >= number_of_alternatives:
                    return alternatives

        # If the requested number of words couldn't be found, return what was found.
        return alternatives or None

    def _find_words_by_adding(self, input_word):
        """ 
            Find words by adding a wildcard between each letter,
            e.g. bird -> ?bird, b?ird, bi?rd, bir?d, bird?
        """
        adder = lambda word, exp, i: word[:i] + exp + word[i:]
        return self._find_words_by_regex_wildcard_match(input_word, adder)

    def _find_words_by_substituting(self, input_word):
        """
            Find words by substituting each letter with a wildcard,
            e.g. bird -> ?ird, b?rd, bi?d, bir?
        """
        substituter = lambda word, exp, i: word[:i] + exp + word[i+1:]
        return self._find_words_by_regex_wildcard_match(input_word, substituter)

    def _find_words_by_regex_wildcard_match(self, input_word, regex_iterator):
        """
            Builds a regex string containing a set of options,
            created by inserting a wildcard using the regex iterator.
            e.g. bird (by adding) -> (?bird|b?ird|bi?rd|bir?d|bird?)
            Searches through the word set and returns a list of matches.
        """
        # Get each individual option, using the iterator.
        regex_generator = (regex_iterator(input_word, r'[a-z]', i)
                                for i in xrange(len(input_word) + 1))

        # Options are seperated by pipes. Spaces are added to aid the search.
        # The regex is surrounded by brackets so that the spaces aren't returned.
        regex = " (%s) " % ('|'.join(regex_generator))

        # Words are seperated by spaces to aid the search.
        word_list = " %s " % (' '.join(self.word_set))

        # Return the results of the search
        return re.findall(regex, word_list)
                                  
    def _find_words_by_removing(self, input_word):
        """
            Find words by removing one letter at a time,
            e.g. bird -> ird, brd, bir
        """
        remover = lambda word, i: word[:i] + word[i+1:]
        return self._find_words_by_iterating_alterations(input_word, remover, xrange(len(input_word) - 1))

    def _find_words_by_swapping(self, input_word):
        """
            Find words by swapping letters in that word,
            e.g. bird -> ibrd, brid, brdi
        """
        swapper = lambda word, i: word[:i] + word[i+1] + word[i] + word[i+2:]
        return self._find_words_by_iterating_alterations(input_word, swapper, xrange(len(input_word) - 1))

    def _find_words_by_iterating_alterations(self, input_word, alterer, iterate_range):
        """
            A generic search method, which alters a word iteratively,
            and returns any matches in the word set.
        """
        # Create generator of all possible words using given alterer and range.
        possible_word_generator = (alterer(input_word, i) for i in iterate_range)

        # Return and of the possible words that are recognised.
        return [word for word in possible_word_generator 
                      if self[word]]

    def _find_closest_words_by_searching(self, input_word):
        """
            Search for closest words by inserting the word into 
            a sorted list of the word set, and returning the words
            on either side.
        """
        # Convert word set to list, add word, and sort the result.
        word_list = sorted(list(self.word_set) + [input_word])

        # Find the position of the word in the sorted list.
        word_index = word_list.index(input_word.lower())

        # Return the two words on either side (if there are any)
        return [word for word in word_list[max(word_index-1, 0):word_index+2] 
                      if word != input_word]


if __name__ == "__main__":
    # Demonstration of use
    def print_word_in_set(word, word_set):
        if word_set[word]:
            print "This word set contains '%s'" % (word)
        else:
            print "This word set doesn't contain '%s'" % (word)

    # Reduced set
    print "Custom word set:"
    print "'bat', 'banana', 'tab', 'dog'"
    collection_of_words = set(['bat', 'banana', 'tab', 'dog'])
    custom_word_set = WordSet(collection_of_words)
    print custom_word_set
    print_word_in_set('banana', custom_word_set)
    print_word_in_set('apple', custom_word_set)
    print

    # Default set
    print "Default word set:"
    default_word_set = WordSet()
    print default_word_set
    print_word_in_set('bungee', custom_word_set)
    print

    # Spelling suggestion
    print "Spelling suggestions:"
    word_set_helper = WordSetHelper(default_word_set)
    print '\n'.join(word_set_helper.get_alternative_words('bungee', 5))
