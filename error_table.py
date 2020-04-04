#!/usr/bin/env python
# coding: utf-8

# Error Table Generation Code Using Python difflib Library
# Scarlett Hwang, April 1st, 2020

# Import libraries
import difflib as dl
import re
import argparse
import os
import pprint as pp

# Parse directory passed with command line argument
parser = argparse.ArgumentParser()
parser.add_argument("directory")
args = parser.parse_args()

# Iterate n file names from the given directory
def iterate_two(iterable, n):
    "s -> (s0,s1,s2,...sn-1), (sn,sn+1,sn+2,...s2n-1), (s2n,s2n+1,s2n+2,...s3n-1), ..."
    return zip(*[iter(iterable)]*n)

# print(sorted(os.listdir(args.directory)))

# Initiate dictionary generation function
def make_dict(list):
    global table
    global total_count
    i = -1

    # iterate through char array
    while i < len(list) - 1:
        total_count += 1
        i += 1
        indicator = list[i][0]
        ch = list[i][2]

        # 1) CORRECT - if original and converted chars match (successfully recognized)
        if indicator == " ":
            chdict = table.get(ch, {})
            chdict[ch] = chdict.get(ch, 0) + 1
            table[ch] = chdict
            continue

        # 2) SUBSTITUTED - if char is not the last character and +/- follows -/+
        if i + 1 < len(list):

            # adjacent character and its indicator
            ch1_ind = list[i + 1][0]
            ch1 = list[i + 1][2]

            # (this letter was added first)
            if (indicator == "+" and ch1_ind == "-"):
                chdict = table.get(ch1, {})
                chdict[ch] = chdict.get(ch, 0) + 1
                table[ch1] = chdict
                i += 1 # increment i and skip next char
                continue

            # (this letter was deleted first)
            if (indicator == "-" and ch1_ind == "+"):
                chdict = table.get(ch, {})
                chdict[ch1] = chdict.get(ch1, 0) + 1
                table[ch] = chdict
                i += 1 # increment i and skip next char
                continue

        # 3) DELETED - if char is not followed by another indicator and this indicator is "-"
        if indicator == "-":
            chdict = table.get(ch, {})
            chdict["Del"] = chdict.get("Del", 0) + 1
            table[ch] = chdict

        # 4) INSERTED - if char is not followed by another indicator and this indicator is "+"
        elif indicator == "+":
            chdict = table.get("Del", {})
            chdict[ch] = chdict.get(ch, 0) + 1
            table["Del"] = chdict

        # 5) OTHER - pass any edge cases for now (never found so far)
        else:
            print("-- something weird going on ---", indicator, ch)
            pass

# Initiate dictionary, read in matching converted and original files from the directory,
# parse them, and make dictionary of the errors
table = {}
total_count = 0
for c, o in iterate_two(sorted(os.listdir(args.directory)), 2):

    ## parameterize the file names for command line inputs
    # parser = argparse.ArgumentParser()
    # parser.add_argument("original")
    # parser.add_argument("converted")
    # args = parser.parse_args()
    o = open((args.directory + "/" + o), "r").read()
    c = open((args.directory + "/" + c), "r").read()

    # Alter format
    # strip new line characters
    o = [x.strip() for x in o.split("\n")]
    c = [x.strip() for x in c.split("\n")]
    o = [x for x in o if x != '']
    c = [x for x in c if x != '']

    # Initiate and generate dictionary for each line
    for ol, cl in zip(o,c):
        n = dl.ndiff(ol, cl)
        list = [i for i in n]
        make_dict(list)
    print("total_count ", total_count)

# Quality check - print dictionary
pp.pprint(table)
print("final total letter count:", total_count)
