#!/usr/bin/env python3
# coding: utf-8

# Probabilities Calculation Functions Using Bayes Theorem
# Scarlett Hwang | April 14th, 2020
##
import json
import pandas as pd
import numpy as np
import argparse
import os
import string
import re


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
        transforms = {}
        total = sum(lettertransforms.values())
        for converted, count in lettertransforms.items():
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
            return -12  # log(1e-9)
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


## ------------- TEST THE CODE -----------------##
# parser = argparse.ArgumentParser()
# parser.add_argument("ver")
# args = parser.parse_args()

parser = argparse.ArgumentParser()
parser.add_argument("table")
args = parser.parse_args()
error_table_fname = args.table

## ---------- load and such
## Here we transform the characters into integer indices to speed up array lookup
table = load_table(error_table_fname)
# create a series of all original characters and converted characters
ochar_list = list(table.keys())
oindex = pd.Series(range(len(ochar_list)), index=ochar_list, dtype="int")  # tell char based on index
ochar = pd.Series(ochar_list, index=range(len(ochar_list)))  # tell index based on char
cchar_set = set()
for k, v in table.items():
    # v is a dict with converted chars as values
    cchar_set |= set(v.keys())
cchar_list = list(cchar_set)
cindex = pd.Series(range(len(cchar_list)), index=cchar_list, dtype="int")  # tell char based on index
cchar = pd.Series(cchar_list, index=range(len(cchar_list)))  # tell index based on char
# create the log-probability table 'prco'
# rows are integer indices for original letters, columns are integer indices for converted letters
# look up integer indices from oindex, cindex series.
prco = np.zeros(shape = (len(ochar), len(cchar))) - 12  # Pr(c|o)
#    -12 -> default entry for non-observed conversion, sort of Bayesian prior
# fill out the table
for oc, convertdict in table.items():
    # v is a dict with converted chars as values
    io = oindex[oc]
    for cc, loglik in convertdict.items():
        jc = cindex[cc]
        prco[io,jc] = loglik
# prco done

## load corpus and transform it into arrays of letter indices
corpus = load_corpus()
corpuslen = np.array(corpus.index.str.len() + 1)  # array of word lengths, including +1 for end marker
maxlen = max(corpuslen)  # max word length, we need it for the 'corpuswords' table
corpuswords = np.zeros(shape = (len(corpus), maxlen), dtype="int") - 1  # table of corpus words in letter index form
#   rows: words, columns: letters, coding is the same as coding of the original characters
print("create corpus letter table")
# should speed up the following... takes a few min currently
for iw, w in enumerate(corpus.index):
    chars = list(w + " ")  # adds space at the end as the end marker
    i = oindex[chars]
    corpuswords[iw, :len(i)] = i
# 

## ---------- run
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
# strip punctuations
tokens = test.replace('-', ' ').split()

# Strip remaining punctuations
punc = str.maketrans('', '', string.punctuation)
tokens = [w.translate(punc) for w in tokens]

for token_conv in tokens[:30]:
    best_ll = -np.Inf
    o = token_conv
    print(token_conv, "->", end=" ")

    tokenchars = list(token_conv + " ")
    if all([c in cindex.index for c in tokenchars]):
        # all token characters are known
        cletters = cindex[tokenchars].values
        for iorig in range(len(corpuswords)):
            minlen = min(len(cletters), corpuslen[iorig])
            p = prco[corpuswords[iorig, :minlen], cletters[:minlen]]  # [original, converted]
            l = sum(p) + corpus.iloc[iorig]
            if l > best_ll:
                best_ll = l
                o = corpus.index[iorig]
        print(o)
    else:
        print(o, ": contains unknown character, not processed")
