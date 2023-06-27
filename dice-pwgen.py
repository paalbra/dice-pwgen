#!/usr/bin/env python3
import logging
import math
import random
import re
import requests
import sys

wordlist_url = "https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt"
password_count = 50
word_count = 6

def parse_wordlist(text):
    text = text.strip() # strip excess whitespace
    lines = text.splitlines()
    words = [line.split()[-1] for line in lines] # expect the last characters on every line to be the word

    # Check for non-unique words
    if len(words) != len(set(words)):
        logging.debug("The word list contains non-unique words!")
        sys.exit(1)
    logging.debug("Number of words:", len(words))

    # Check that the wordlist contains the correct amount of words
    dice_count = math.log(len(words), 6)
    logging.debug("Number of dice is:", dice_count)
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
    response = requests.get(wordlist_url)
    wordlist = parse_wordlist(response.text)

    if wordlist is None:
        print("Unable to properly parse wordlist.")
        sys.exit(1)

    for x in range(password_count):
        print(" ".join(random.sample(wordlist, word_count)))
