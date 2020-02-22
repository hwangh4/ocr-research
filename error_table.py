#!/usr/bin/env python3
# coding: utf-8

# # OCR Common Error Unigram Table Script
# ### Eviction Study - Automated Optical Character Recognition Correction Algorithm Research
#
# Author: Scarlett Heeyeon Hwang
#
# (currently handles only substitution and deletion)
#
# January 20th, 2020

###---------------------- Import libraries ----------------------###
import numpy as np
import pandas as pd
import string
import prettytable as pt
import argparse
import pprint as pp

parser = argparse.ArgumentParser()
parser.add_argument("original")
parser.add_argument("converted")
args = parser.parse_args()


###----------------------- Generate Table -----------------------###

# row - original
# column - converted
# 1. Splice all possible ascii characters
all_ascii = string.printable

# Create row names with None value for counting up deletions
letters = list(all_ascii[:-5])
letters.append("None")


# 2. Generate table
t = pd.DataFrame(0, letters, letters)

###------ Create Unigram Chart from Original and Converted File (main) ------###

# We assume the length for conv and orig are equal at this point
def main(orig_name, conv_name, t):
    orig = open(orig_name, "r").read()
    conv = open(conv_name, "r").read()

    i = 0

    for j in range(len(conv)):
        if (i < len(orig) and orig[i] != conv[j]):
            curr = i
            i = same_char_at_index(i, j, orig, conv)

            if i is None:
                t.loc["None", conv[j]] += 1
                i = curr
                continue
            if orig[i] == "H":
                print(conv[j-5:j+5])

            if i > curr: # char was deleted
                while i > curr:
                    try:
                        t.loc[orig[curr], "None"] += 1
                    except:
                        pass
                    curr += 1
                try:
                    t.loc[orig[i], conv[j]] += 1
                except:
                    pass
            else:
                try:
                    t.loc[orig[i], conv[j]] += 1
                except:
                    pass
        else:
            try:
                t.loc[orig[i], conv[j]] += 1
            except:
                pass
        i += 1

def same_char_at_index(i, j, orig, conv):
    """
    find if there is a similar character (as in 'orig'
    at position i) in 'conv' at position [j ... j+3]
    """
    count = 0  # position relative to j
    index = i  # copy of i for not to overwrite i
    while (count < 3 and index < len(orig)):
        if (orig[index] == conv[j]):
            return(index)
        else:
            index += 1
            count += 1
    return None

test = pd.DataFrame(0, ("a", "b", "c", "d", "e", " "),
                   ("a", "b", "c", "d", "e", " ", "None"))
main(args.original, args.converted, t)

d = {c: dict(t.loc[c][t.loc[c] != 0]) for c in t.index if t.loc[c].sum() > 0}
pp.pprint(d)

# ### Run test

#main("moby_dick.txt", "moby_dick-converted.txt", t)
