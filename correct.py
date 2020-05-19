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

## ---------- load corpus ----------
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


## -------------  -----------------##

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


## ------------- LOGLIKE -----------------##

def loglik():
    pass


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
        #print(ve)
        return 0

# search corpus
def search_dict(token_conv):
    best = -np.Inf
    o = token_conv
    for token_orig in corpus.index:
        l = word_based_pr(token_conv, token_orig) + corpus[token_orig]
        if l > best:
            best = l
            o = token_orig

    result_list.append(zip(o, best))

def log_result(result):
    # This is called whenever foo_pool(i) returns a result.
    # result_list is modified only by the main process, not the pool workers.
    print(result)
    result_list.append({result[0]: result[1]})

## ------------- TEST THE CODE -----------------##
# parser = argparse.ArgumentParser()
# parser.add_argument("ver")
# args = parser.parse_args()

parser = argparse.ArgumentParser()
parser.add_argument("table")
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

# Example test for debugging
test = """
ćontragravity lorries were driffing back and forth, scattering
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

# test = open(args.textfile).read()  # uncomment for input command-line arg

tokens = test.replace('-', ' ').split()

# Strip remaining punctuations
punc = str.maketrans('', '', string.punctuation)
tokens = [w.translate(punc) for w in tokens]

pool_size = 2
p = Pool()

for token_conv in tokens:
    best_ll = -np.Inf
    print(token_conv, "->", end=" ")

    if not re.match('^[a-zA-Z_]+$', token_conv):   # if special character is found
        print(token_conv, " (skipped - contains accented character)")
    else:
        ## check to correct prior depending on the case
        if token_conv.islower():
            prior = corpus_lowercase
        elif token_conv.istitle():
            prior = corpus_capitalized
        elif token_conv.isupper():
            prior = corpus_uppercase
        else:
            # no clear case, let's do some heuristics
            nupper = sum(1 for c in token_conv if c.isupper())
            nlower = len(token_conv) - nupper
            if nupper > nlower:
                prior = corpus_uppercase
            else:
                prior = corpus_lowercase
        # result_list = {}
        for token_orig in prior.index:
            l = word_based_pr(token_conv, token_orig) + prior[token_orig]
            if l > best_ll:
                best_ll = l
                o = token_orig

        # result_list.append(zip(o, best))
        # p.apply_async(search_dict, args = (token_conv, ))
        print(o)

        # max_value = max(result_list.values())  # maximum value
        # max_key = [k for k, v in result_list.items() if v == max_value]
        # print(max_key, " is max key")
p.close()
p.join()
# print(result_list)


## ------------- COMMAND-LINE ARGUMENT DIRECTORY --------##
# Run on a specific folder - uncomment when code is ready
# for c, o in iterate_two(sorted(os.listdir(args.directory)), 2):
#     o = open((args.directory + "/" + o), "r").read()
#     c = open((args.directory + "/" + c), "r").read()
#
#     for i, j in zip(o.split(), c.split()):
#         print(i, j)
#         print(word_based_pr(i, j))
