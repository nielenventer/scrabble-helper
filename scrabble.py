#!/usr/bin/env python

"""
Command line interface for scrabble helper.
Run in command line with --help for more information and examples

Requires Python 2.7.*, not compatible with Python 3.

Version: 1.0
Author: Nielen Venter
"""

import argparse, textwrap
import sys

from word_scrabblers import WordScrabbleCalculator, WordScrabbleHelper
from word_sets import WordSet, WordSetHelper

#------------- Argument Parsing ----------------#

# Initialise argument parser, with introductory description
parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=textwrap.dedent('''\

This is a command line interface for a Scrabble helper.

 '''), epilog=textwrap.dedent('''\
 
 Examples of running the script:
 ----------------------------- 
    1) Get possible words with current tiles (tiles used: 'ska '):
        python scrabble.py "ska "

    2) Get possible words and suggestions for words to target.
        python scrabble.py "ska " -s

Usage
--------------------------------
Software can be run using:
    'python scrabble.py' or
    './scrabble.py' from the local directory.
Alternatively it can be linked to /usr/local/bin to be called from anywhere.
 ''')
                                 )

# 1st argument is the tiles to analyse.
parser.add_argument("letters", help="Your tiles, up to a max of 7. (' ' for blank).")

# Switches argument group (optional) allows various stages of the processing to be disabled.
group = parser.add_argument_group('Switches')
group.add_argument("-s", help="Turn on target word suggestions.", action="store_true")

# Make sure some arguments are given.
if len(sys.argv) == 1:
    print "No inputs given. For detailed usage please append -h or --help "
    sys.exit(1)

args = parser.parse_args()

#-------------- Word Analysis ------------------#

if not args.s:
    # Print possible words with current tiles.
    set_of_all_words = WordSet()
    scrabble_calc = WordScrabbleCalculator(args.letters, set_of_all_words)
    print scrabble_calc
else:
    # Print possible words with suggestions.
    set_of_all_words = WordSetHelper()
    scrabble_helper = WordScrabbleHelper(args.letters, set_of_all_words)
    print scrabble_helper
