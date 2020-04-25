#!/usr/bin/env python3
# coding: utf-8

# Probabilities Calculation Functions Using Bayes Theorem
# Scarlett Hwang | April 14th, 2020
import json
import pandas as pd
import numpy as np
import argparse
import os

def load_corpus():
    """
    load word frequency corpus
    """
    print("Loading corpus")
    # if (args.ver == "scarlett"):
    #     a = pd.read_csv("frequency-corpus.txt", sep="\t",
    #                     keep_default_na=False, na_values=[""], names=["word", "count"])
    # else:
    a = pd.read_csv("corpus/frequency-corpus.txt.bz2", sep="\t",
                    keep_default_na=False, na_values=[""])
    c = pd.Series(a["count"].values, index=a.word)
    c = np.log(c) - np.log(sum(c))
    return c

def load_table():
    """
    load the count dict from file.
    eventually does smoothing and other things
    """
    table = json.load(open("table.json"))
    return table


def char_based_pr(conv, orig):
    """
    return log Pr(converted|original) for individual letters
    the corresponding counts are based on dict 'table'
    """
    if orig in table:
        if conv in table[orig]:
            p = table[orig][conv] / sum(table[orig].values())
            return np.log(p)
        else:
            return 1e-8
    else:
        raise ValueError("Crap, I have never seen this character in the table" + orig)

def loglik():
    pass

def word_based_pr(conv, orig):
    """
    return log Pr(converted|original) for individual words/tokens/other
    multiletter structures
    the corresponding counts are based on dict 'table', used by 'char_based_pr'
    """
    try:
        word_p = 0
        for i, j in zip(orig, conv):
            word_p = word_p + char_based_pr(j, i)
        return(word_p)
    except ValueError as ve:
        print(ve)
        return 0


## ------------- TEST THE CODE -----------------##
parser = argparse.ArgumentParser()
parser.add_argument("ver")
args = parser.parse_args()

table = load_table()
corpus = load_corpus()
print(table)
#
# examples = [('applc', 'apple'), ('Utter', 'Uller'), ("4.", "1."),
#             ("tie", "the"), ("tbe", "the")]
# print("A few examples")
# for conv, orig in examples:
#     print("Pr(", conv, "|", orig, ") =", word_based_pr(conv, orig))
#
test = """
contragravity lorries were driffing back and forth, scattering
fertilizer, mainly nitrates from Mimir or Yggarasill. There were stit
a good number of animal-drawn plows ahd harrows in use, however.

As planots went, Uiler was no bargain, he thought soury.Attimes, he
wished he had never followed the lure of rapid promotion and
fantastically high pay and left the Federation regulars for the army

at the Uiler Company, the hadn't e'd probably be a colonel, zt

five thousand sols a year, but maybe it would be better to be a
middle-aged colonel cn a decent planet-Odin, with its two moons,
"""
tokens = test.split()
for token_conv in tokens:
    best_ll = -np.Inf
    o = token_conv
    print(token_conv, "->", end=" ")
    for token_orig in corpus.index:
        l = word_based_pr(token_conv, token_orig) + corpus[token_orig]
        if l > best_ll:
            best_ll = l
            o = token_orig
    print(o)
