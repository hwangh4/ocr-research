#!/usr/bin/env python3
# coding: utf-8

# Probabilities Calculation Functions Using Bayes Theorem
# Scarlett Hwang | April 14th, 2020
import json
import pandas as pd
import numpy as np
import argparse
import os
import string
import re
from multiprocessing import Pool
from functools import partial


## ---------- Load corpus ---------- ##
def load_corpus():
    """
    load word frequency corpus
    return a dicts of corresponding word log probabilites
    """
    print("Loading corpus")
    a = pd.read_csv("corpus/frequency-corpus.txt.bz2", sep="\t",
                    keep_default_na=False, na_values=[""])
    c = pd.Series(a["count"].values, index=a.word)
    c = np.log(c) - np.log(sum(c))
    return c


## ------------- Load table -----------------##

def load_table(fname, log=True):
    """
    load the count dict from file.
    eventually does smoothing and other things
    """
    table = json.load(open(fname))
    if not log:
        # mainly for debugging: it is handy to have the original table
        return table
    grandtotal = 0
    logtable = {}
    for letter, lettertransforms in table.items():
        # letter: original characters,
        # lettertransforms: dict of what they become
        transforms = {}
        total = sum(lettertransforms.values())
        for converted, count in lettertransforms.items():
            # converted: original was seen as converted to these characters
            # count: how many times each converted was seen
            transforms[converted] = np.log(count) - np.log(total)
        logtable[letter] = transforms
        grandtotal += total
    print("  In total", grandtotal, "transformations")
    return logtable


## ------------- CHARACTER PROBABILITY CALCULATION -----------------##

def char_based_pr(conv, orig):
    """
    return log Pr(converted|original) for individual letters
    the corresponding counts are based on dict 'table'
    """
    if orig in table:
        if conv in table[orig]:
            p = table[orig][conv]
            return p
        else:
            return -20.72  # log(1e-9)
    else:
        raise ValueError("Crap, I have never seen this character in the table" + orig)


## ------------- FULL WORD PROBABILITY CALCULATION -----------------##
# Pr(w1|w2)
# w2: Original word
# w1: Converted word

def word_based_pr(conv, orig):
    """
    return log Pr(converted|original) for individual words/tokens/other
    multiletter structures
    the corresponding counts are based on dict 'table', used by 'char_based_pr'
    """
    try:
        # are these words of the same length?
        # if not, add a space to the shorter one
        # otherwise zip() will only include the first few characters
        if len(orig) == len(conv):
            pair = zip(orig, conv)
        elif len(conv) < len(orig):
            pair = zip(orig, conv + " ")
        elif len(orig) < len(conv):
            pair = zip(orig + " ", conv)
        # loop over original-converted characters
        word_p = 0
        for o, c in pair:
            word_p += char_based_pr(c, o)
        return(word_p)
    except ValueError as ve:
        return 0


## -------- Search dictionary (used for parallelizing) --------##
def search_dict(token_conv, case, token_orig):
    if case == "l":
        ll = word_based_pr(token_conv, token_orig) + corpus_lowercase[token_orig]
    elif case == "c":
        ll = word_based_pr(token_conv, token_orig) + corpus_capitalized[token_orig]
    elif case == "u":
        ll = word_based_pr(token_conv, token_orig) + corpus_uppercase[token_orig]
    return ll

## ------------- MAIN: TEST THE CODE -----------------##
parser = argparse.ArgumentParser()
parser.add_argument("table")
parser.add_argument('--parallel', '-p', type=int, default=2,
                    help='Level of parallelism')
# parser.add_argument("textfile")   # uncomment for input command-line arg
args = parser.parse_args()

error_table_fname = args.table

alphaC = 0.1  # probability for capitalized
alphaU = 0.001  # probability for upper case
table = load_table(error_table_fname)
corpus = load_corpus()
corpus_lowercase = corpus - np.log(1 + alphaC + alphaU)
corpus_lowercase.index = corpus.index.str.lower()
corpus_capitalized = corpus - np.log(1 + alphaC + alphaU) + np.log(alphaC)
corpus_capitalized.index = corpus.index.str.title()
corpus_uppercase = corpus - np.log(1 + alphaC + alphaU) + np.log(alphaU)
corpus_uppercase.index = corpus.index.str.upper()
## other parameters, to be specified

# -----------SHORT DEBUGGING TEXT--------
# test = """
# ćontragravity lorries were driffing back and forth,
# """
# ----------LONG DEBUGGING TEXT----------
test = """
ćontragravity Lorries were driffing back and forth, scattering
fertilizer, mainly nitrates from Mimir or Yggarasill. There were stit
a good number of animal-drawn plows ahd harrows in use, however.

As planots went, Uiler was no bargain, he thought soury.Attimes, he
wished he had never followed the lure of rapid promotion and
fantastically high pay and left the Federation regulars for the army

at the Uiler Company, the hadn't e'd probably be a colonel, zt

five thousand sols a year, but maybe it would be better to be a
middle-aged colonel cn a decent planet-Odin, with its two moons,
"""
#strip punctuations

# ----------ACTUAL INPUT----------
# test = open(args.textfile).read()  # uncomment for input command-line arg

# Split hyphenated words
tokens = test.replace('-', ' ').split()

# Strip remaining punctuations
punc = str.maketrans('', '', string.punctuation)
tokens = [w.translate(punc) for w in tokens]

# Create multiprocessing pool
pool_size = args.parallel
p = Pool(processes = pool_size)
print("using %d" % p._processes + "-fold parallelism")

for token_conv in tokens:
    best_ll = -np.Inf
    print(token_conv, "->", end=" ")

    if not re.match('^[a-zA-Z_]+$', token_conv):   # if special character is found
        print(token_conv, " (skipped - contains accented character)")
    else:
        if token_conv.islower():
            case = "l"
            prior = corpus_lowercase
        elif token_conv.istitle():
            case = "c"
            prior = corpus_capitalized
        elif token_conv.isupper():
            case = "u"
            prior = corpus_uppercase
        else:
            # no clear case, let's do some heuristics
            nupper = sum(1 for c in token_conv if c.isupper())
            nlower = len(token_conv) - nupper
            if nupper > nlower:
                case = "u"
                prior = corpus_uppercase
            else:
                case = "u"
                prior = corpus_lowercase
        best = -np.Inf
        # search corpus in parallel
        result = p.map(partial(search_dict, token_conv, case), prior.index)

        i = np.argmax(result)
        print(prior.index[i], "(%1.3f" % result[i] + ")")

p.close()
