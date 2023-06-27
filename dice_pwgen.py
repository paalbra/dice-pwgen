#!/usr/bin/env python3
import argparse
import logging
import math
import random
import sys

import requests

WORDLIST_URL = "https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt"


def parse_wordlist(text):
    text = text.strip()  # strip excess whitespace
    lines = text.splitlines()
    words = [line.split()[-1] for line in lines]  # expect the last characters on every line to be the word

    logging.debug("Number of words: %d", len(words))

    # Check for non-unique words
    if len(words) != len(set(words)):
        raise Exception("The word list contains non-unique words!")

    # Check that the wordlist contains a fair amount of words
    word_count = len(words)
    if word_count < 1000:
        raise Exception("There are too few words in the word list: %d" % word_count)

    # Check that the wordlist contains the correct amount of words
    dice_count = math.log(len(words), 6)
    logging.debug("Number of dice is: %d", dice_count)
    if not (dice_count.is_integer() and dice_count > 0):
        raise Exception("The number of dice is not an integer: %.2f" % dice_count)

    # Check the average word length
    avg_word_length = sum(len(word) for word in words) / len(words)
    if avg_word_length < 4:
        raise Exception("Average word length is to small: %.2f" % avg_word_length)

    # All OK. Return the words
    return words


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="Verbose logging", action="store_true")
    parser.add_argument("-w", "--words", type=int, help="Number of words per password", default=6)
    parser.add_argument("-p", "--passwords", type=int, help="Number of passwords printed", default=50)
    parser.add_argument("-s", "--separator", help="Word separator", default=" ")
    args = parser.parse_args()

    if args.verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.WARNING

    logging.basicConfig(level=log_level)

    try:
        response = requests.get(WORDLIST_URL, timeout=10)
        response.raise_for_status()
    except Exception as e:
        logging.error("Unable to get wordlist (%s): %s", WORDLIST_URL, str(e))
        sys.exit(1)

    try:
        wordlist = parse_wordlist(response.text)
    except Exception as e:
        logging.error(str(e))
        sys.exit(1)

    for x in range(args.passwords):
        print(args.separator.join(random.sample(wordlist, args.words)))
