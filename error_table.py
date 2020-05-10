#!/usr/bin/env python3
# coding: utf-8

# Error Table Generation Code Using Python difflib Library
# Scarlett Hwang, April 1st, 2020

# Import libraries
import difflib as dl
import re
import argparse
import os
import pprint as pp
import json


# Parse directory passed with command line argument
parser = argparse.ArgumentParser()
parser.add_argument("directory")
args = parser.parse_args()

def deleted(diffs, i):
    """
    extract a consequtive sequence of deleted characters from diff list at index i
    """
    d = list()
    while  (i < len(diffs)) and (diffs[i][0] == '-'):
        # note: first test length and thereafter the character!
        d.append(diffs[i][2])
        i += 1
    return d


def inserted(diffs, i):
    """
    extract a consequtive sequence of inserted characters from diff list at index i
    """
    d = list()
    while  (i < len(diffs)) and (diffs[i][0] == '+'):
        d.append(diffs[i][2])
        i += 1
    return d


# Iterate n file names from the given directory
def iterate_two(iterable, n):
    "s -> (s0,s1,s2,...sn-1), (sn,sn+1,sn+2,...s2n-1), (s2n,s2n+1,s2n+2,...s3n-1), ..."
    return zip(*[iter(iterable)]*n)

# Initiate dictionary generation function
def make_dict(list):
    """
    Create the dictionary of character translations
    inputs:
    list: list of trigrams from ndiff
    """
    global table
    global total_count
    i = 0
    # iterate through char array
    while i + 1 < len(list):
        indicator = list[i][0]
        ch = list[i][2]

        # 1) CORRECT - if original and converted chars match (successfully recognized)
        if indicator == " ":
            chdict = table.get(ch, {})
            chdict[ch] = chdict.get(ch, 0) + 1
            table[ch] = chdict
            i += 1
            total_count += 1
            continue

        ## 2) SUBSTITUTED - if char is not the last character and +.. is folowed by -.. or the way around
        ## we make two lists of successive insertions and deletions, and thereafter
        ## assume that each deletion was replaced by insertion
        ## The leftover deletions/insertions are assumed to be just that: deletions or insertions
        if i + 1 < len(list):
            ## create two lists--ilist and dlist--for inserted and deleted
            ## characters
            if indicator == "-":
                dlist = deleted(list, i)
                ilist = inserted(list, i + len(dlist))
            elif indicator == "+":
                ilist = inserted(list, i)
                dlist = deleted(list, i + len(ilist))
            ## walk over the lists and mark transforms
            ic = -1
            for ic in range(min(len(ilist), len(dlist))):
                cho = dlist[ic]  # original character
                chc = ilist[ic]  # converted character
                chdict = table.get(cho, {})
                chdict[chc] = chdict.get(chc, 0) + 1
                table[cho] = chdict
            ## check if any leftover insertions/deletions
            ## do we have more deletions?
            ic += 1
            while ic < len(dlist):
                cho = dlist[ic]
                chdict = table.get(cho, {})
                chdict["Del"] = chdict.get("Del", 0) + 1
                table[cho] = chdict
                ic += 1
            ## or maybe more insertions?
            while ic < len(ilist):
                chc = ilist[ic]
                chdict = table.get("Del", {})
                chdict[chc] = chdict.get(chc, 0) + 1
                table["Del"] = chdict
                ic += 1
            i += len(dlist) + len(ilist)
            total_count += len(dlist)

        # 5) OTHER - pass any edge cases for now (never found so far)
        else:
            print("-- something weird going on ---", indicator, ch)
            i += 1
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
        n = list(dl.ndiff(ol, cl))
        make_dict(n)
    print("total_count ", total_count)

outfname = args.directory + ".json"
with open(outfname, 'w') as file:
    file.write(json.dumps(table))
print("output written to", outfname)

print("final total letter count:", total_count)
