import string, re
import itertools
from collections import Counter # A Counter is a histogram of the elements in a collection
from word_set import WordSet, WordSetHelper


class WordScrabbleCalculator(object):
    """
        A class to calculate the value of a given word (or set of letters)
        in Scrabble. Can be used to generate all makeable words.
    """
 
    letter_values = {'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 
                     'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 
                     'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 
                     'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 
                     'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10, ' ': 0}

    def __init__(self, word, word_set=None):
        # Word must be a string
        if (type(word) is not str):
            raise TypeError('String expected.')
        # Word must not contain any punctuation or digits.
        if any(letter in (string.punctuation + string.digits) for letter in word):
            raise TypeError('No punctuation or digits accepted.')
        # Word length must be 7 or less (max number of Scrabble tiles).
        if len(word) > 7:
            raise TypeError('Input length should be 7 or less.')

        self.word = word

        # If a word set was given, use it. Else create a new one.
        if word_set is not None:
            if not isinstance(word_set, WordSet):
                raise TypeError('WordSet expected.')
            self.word_set = word_set  
        else:
            self.word_set = WordSet()

    def __repr__(self):
        print_string = "Letters: '%s'\n" % (self.word)
        print_string += "\nWith these letters you can make:\n"
        suggestions = self.get_suggestions(5)

        print_string += '\n'.join(self._get_possible_word_description(suggestion) 
                                    for suggestion in suggestions)

        return print_string

    def _get_possible_word_description(self, word):
        """
            Get a readable description of the given word.
        """
        return "- %s (%d points)" % (word, self._get_score(word, self.word))

    def _get_score(self, word, available_letters=None):
        """
            Returns the scrabble value of a given word.
            Available letters can optionally be given to only
            calculate the score based on those (mainly used to
            account for letters added by blank tiles).
        """
        if available_letters:
            # Remove letters that aren't available. A Counter is used to handle
            # more than one of the same letter in a letter set
            word = ''.join(list((Counter(word) & Counter(available_letters)).elements()))
        return sum(self.letter_values[letter] for letter in word)

    def _get_anagrams(self, word):
        """
            Get all anagrams of a given word or set of letters.
        """
        anagrams = []
        # Iterate through all permutations of the letters.
        for permutation in itertools.permutations(word):
            potential_anagram = ''.join(permutation)
            # Store recognised words.
            if self.word_set[potential_anagram]:
                anagrams.append(potential_anagram)

        return anagrams

    def get_possible_words(self):
        """
            Get all the words that can be made with a
            given word or set of letters.
        """
        possible_words = []
        number_of_blanks = self.word.count(' ')

        if number_of_blanks:
            # Remove blanks from result (each one adds unnecessary permutations).
            stripped_word = self.word.translate(None, ' ')
            # Get all possible combinations that the blanks can provide.
            letter_combinations = itertools.combinations(string.ascii_lowercase, number_of_blanks)
            # Add all the combinations to the original word.
            input_words = [(stripped_word + ''.join(letters)) for letters in letter_combinations]
        else:
            input_words = [self.word]

        # Go through words (any blanks lead to multiple variations).
        for word in input_words:
            # For each combination of letter subsets, get all the anagrams of that combination.
            # Start at 2 since thats the minimum Scrabble word length.
            for i in xrange(2, len(word) + 1):
                for combo in itertools.combinations(word, i):
                    possible_words.extend(self._get_anagrams(''.join(combo)))

        # Remove any duplicates
        return list(set(possible_words))

    def get_suggestions(self, n):
        """
            Get n word suggestions that can be made with the given word
            or set of letters. Result is ordered from highest scoring to lowest.
        """
        sorter = lambda x: self._get_score(x, self.word)
        return sorted(self.get_possible_words(), key=sorter, reverse=True)[:n]


class WordScrabbleHelper(WordScrabbleCalculator):
    """
        A class combining the WordScrabbleCalculator and WordCorrector
        to provide improved assistance to Scrabble players.
        Gives a list of possible words, ordered by their Scrabble scores,
        as well as some suggestions for words to try go for, also ordered
        the same way.
    """
    def __init__(self, word, word_set=None):
        # Word is handled the same way, but word_set needs to be a WordSetHelper.
        super(WordScrabbleHelper, self).__init__(word, None)

        # If a word set was given, use it. Else create a new one.
        if word_set is not None:
            if not isinstance(word_set, WordSet):
                raise TypeError('WordSet expected.')
            # If a WordSet was passed in, upgrade it.
            if not isinstance(word_set, WordSetHelper):
                self.word_set = WordSetHelper(word_set())
            else:
                self.word_set = word_set  
        else:
            self.word_set = WordSet()

        # self.word_set._search_order = self.word_set._search_order[2:]
    
    def __repr__(self):
        print_string = super(WordScrabbleHelper, self).__repr__()
        
        new_suggestions = self.get_alternative_suggestions(5)
        if new_suggestions:
            print_string += "\n\nPerhaps you should try going for:\n"
            print_string += '\n'.join(self._get_suggestion_description(suggestion) 
                                            for suggestion in new_suggestions)
        else:
            print_string += "\nNo idea what to go for."

        return print_string

    def get_alternative_suggestions(self, n):
        """
            Gets a list of words that are worth attempting to get,
            based on the current word or set of letters.
        """
        # Get both possible and alternative words.
        possible_words = self.get_possible_words()
        # There are many alternative words, so use a generator.
        # Since the search methods are based on miss-spellings, 
        alternative_words = (alternative for word in possible_words
                                          for alternative in self.word_set.get_alternative_words(word))
 
        def limiter(iterator, limit):
            """A limiter function to stop the generator after a given number of iterations. 
                I love Python."""
            for i in xrange(limit):
                yield next(iterator)
            raise StopIteration

        # Suggestions are only valid if they aren't possible, and are within the word length limits.
        suggestion_valid = lambda x: (x not in possible_words) and (1 < len(x) <= 7)
        # Put twice the target number in the limiter, in case there are invalid suggestions.
        suggestions = [word for word in limiter(alternative_words, 2*n) if suggestion_valid(word)]

        # Return suggestions, ordered by their highest possible Scrabble score value.
        sorter = lambda x: self._get_suggestion_score(x)[-1]
        return sorted(suggestions, key=sorter, reverse=True)[:n]

    def _get_suggestion_description(self, suggestion):
        """
            Get a readable description of the given suggestion.
        """
        # Get information about the suggestion
        number_of_blanks = self.word.count(' ')
        letters_needed = self._get_letters_needed(suggestion)
        score = self._get_suggestion_score(suggestion)
        
        description = "- %s. You need" % suggestion

        # Print letters needed (only a subset of these is required if there are any blanks).
        if number_of_blanks:
            description += " %d of" % (len(letters_needed) - number_of_blanks)
        description += " these letter(s): [%s]" % (','.join(letters_needed))

        # Print the score of the word (might be a range if there are any blanks).
        description += ", for a total score of %d" % (score[0])
        if (len(score) > 1) and (score[0] != score[-1]):
            description += " to %d" % (score[-1])

        return description

    def _get_letters_needed(self, suggestion):
        """
            Get the letters required to make a suggested word.
            A Counter is used to preserve words containing more than 
            one of the same letter.
        """
        return list((Counter(suggestion) - Counter(self.word)).elements())

    def _get_suggestion_score(self, suggestion):
        """
            Get the score of a word suggestion. If the current
            word contains a blank, this will be a range.
        """
        number_of_blanks = self.word.count(' ')
        if not number_of_blanks:
            return (self._get_score(suggestion),)
        else:
            # Get the letters (and number thereof) required to make the suggestion.
            letters_needed = self._get_letters_needed(suggestion)
            # Subtract the number of blanks from the number of letters needed.
            number_of_letters_needed = len(letters_needed) - number_of_blanks

            # Sort the letters by their Scrabble value.
            values = sorted(letters_needed, key=lambda x: self.letter_values[x])

            # Get the least and most valuable letter combos (depending on how many are needed).
            least_valuable = values[:number_of_letters_needed]
            most_valuable = values[-number_of_letters_needed:]

            # Calculate the resulting scores, if these numbered were added.
            score_without = lambda x: self._get_score(suggestion) - self._get_score(''.join(x))
            lower_score, highest_score = score_without(most_valuable), score_without(least_valuable)

            # Return the result as a tuple.
            return (lower_score, highest_score)


if __name__ == "__main__":
    # Example of usage
    set_of_all_words = WordSet()

    NewWord1 = WordScrabbleHelper('niele ', set_of_all_words)
    print NewWord1
