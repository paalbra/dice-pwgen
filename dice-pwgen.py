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

    # Check for non-unique words
    if len(words) != len(set(words)):
        logging.error("The word list contains non-unique words!")
        sys.exit(1)
    logging.debug("Number of words: %d", len(words))

    # Check that the wordlist contains the correct amount of words
    dice_count = math.log(len(words), 6)
    logging.debug("Number of dice is: %d", dice_count)
    if not dice_count.is_integer():
        print("The number of dice is not an integer!")
        sys.exit(1)

    # Check the average word length
    avg_word_length = sum([len(word) for word in words]) / len(words)
    if avg_word_length < 4:
        print("Average word length is to small:", avg_word_length)
        sys.exit(1)

    # All OK. Return the words
    return words


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="Verbose logging", action="store_true")
    parser.add_argument("-w", "--words", type=int, help="Number of words per password", default=6)
    parser.add_argument("-p", "--passwords", type=int, help="Number of passwords printed", default=50)
    args = parser.parse_args()

    if args.verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.WARNING

    logging.basicConfig(level=log_level)

    response = requests.get(WORDLIST_URL)
    wordlist = parse_wordlist(response.text)

    if wordlist is None:
        print("Unable to properly parse wordlist.")
        sys.exit(1)

    for x in range(args.passwords):
        print(" ".join(random.sample(wordlist, args.words)))
