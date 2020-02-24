#!/usr/bin/env python3
# coding: utf-8

# # OCR Common Error Unigram Table Script
# ### Eviction Study - Automated Optical Character Recognition Correction Algorithm Research
#
# Author: Scarlett Heeyeon Hwang
#
# (VER 3 - currently handles insertions, substitutions, and deletions)
#
# January 20th, 2020

###---------------------- Import libraries ----------------------###
import numpy as np
import pandas as pd
import string
import prettytable as pt
import argparse
import pprint as pp

## parameterize the file names for command line inputs
parser = argparse.ArgumentParser()
parser.add_argument("original")
parser.add_argument("converted")
args = parser.parse_args()


###----------------------- Generate Table -----------------------###
## Generate the "big" table with all possible English ascii letters that could
## be read in by tesseract
## row - original / column - converted

## 1. Splice all possible ascii characters
all_ascii = string.printable

## 2. Create row names with "Del" value for counting up insertions and deletions
letters = list(all_ascii[:-5])
letters.append("Del")


## 3. Generate table
t = pd.DataFrame(0, letters, letters)


###------ Create Unigram Chart from Original and Converted File (main) ------###
## We assume the length for conv and orig are equal at this point
## Params: orig_name(file) - original file of text
##         conv_name(file) - converted file of text after OCR (contains errors)

def main(orig_name, conv_name, t):
    orig = open(orig_name, "r").read()
    conv = open(conv_name, "r").read()

    i = 0   # set initial index for orig

    # compare orig in function of conv (REVISE)
    for j in range(len(conv)):
        # if current char of orig and conv are not equal
        if (i < len(orig) and orig[i] != conv[j]):
            curr = i    # temp to prevent overwriting current index
            i = same_char_at_index(i, j, orig, conv)

            # 1. if *insertion* occured so returned value is None (REVISE)
            if i is None:
                if conv[j] in t.columns:
                    t.loc["Del", conv[j]] += 1
                i = curr
                continue

            # 2. if *deletion* occured
            if i > curr:
                # log every deleted letters in a row
                while i > curr:
                    # count up for [orig, Del] if our ascii letters list
                    #  contains orig char
                    try:
                        t.loc[orig[curr], "Del"] += 1
                    except:
                        pass
                    curr += 1

                ## DO WE NEED THIS??????
                # try:
                #     t.loc[orig[i], conv[j]] += 1
                # except:
                #     pass

            # 3. if *substitution* occured
            else:
                try:
                    t.loc[orig[i], conv[j]] += 1
                except:
                    pass

        # if current char of orig and conv are equal
        else:
            try:
                t.loc[orig[i], conv[j]] += 1
            # pass if the char is not in our ascii letters list
            except:
                pass

        # increment orig's index
        i += 1


###------------- Move index of original text to correct position ------------###
## Return (int): updated index if deletion occured
##               None if substitution occured
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


###--------------------------- Run unit test --------------------------------###
test = pd.DataFrame(0, ("a", "b", "c", "d", "e", " "),
                   ("a", "b", "c", "d", "e", " ", "None"))

###-------------------------- Run actual test -------------------------------###
main(args.original, args.converted, t)


###--------------------------- Run unit test --------------------------------###
d = {c: dict(t.loc[c][t.loc[c] != 0]) for c in t.index if t.loc[c].sum() > 0}
pp.pprint(d)

count = 0
