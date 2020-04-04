#!/usr/bin/env python
# coding: utf-8

# Error Table Generation Code Using Python difflib Library
# Scarlett Hwang, April 1st, 2020

# Import libraries
import difflib as dl
import re
import argparse
import os

# Call test texts
# 50 lines
# o = open("moby_dick-orig/moby_dick-orig-chunk-aa.txt", "r").read()
# c = open("moby_dick-orig/moby_dick-orig-chunk-aa-converted.txt", "r").read()

# 10 lines
# o = open("moby_dick-10/moby_dick-orig-chunk-ab.txt", "r").read()
# c = open("moby_dick-10/moby_dick-orig-chunk-ab-converted.txt", "r").read()

parser = argparse.ArgumentParser()
parser.add_argument("directory")
args = parser.parse_args()

def iterate_two(iterable, n):
    "s -> (s0,s1,s2,...sn-1), (sn,sn+1,sn+2,...s2n-1), (s2n,s2n+1,s2n+2,...s3n-1), ..."
    return zip(*[iter(iterable)]*n)

# print(sorted(os.listdir(args.directory)))

for conv, orig in iterate_two(sorted(os.listdir(args.directory)), 2):
    print(conv)
    print(orig)
    print("---------------")

# ## parameterize the file names for command line inputs
# parser = argparse.ArgumentParser()
# parser.add_argument("original")
# parser.add_argument("converted")
# args = parser.parse_args()
# o = open(args.original, "r").read()
# c = open(args.converted, "r").read()
#
# # Alter format
# # strip new line characters
# o = [x.strip() for x in o.split("\n")]
# c = [x.strip() for x in c.split("\n")]
# o = [x for x in o if x != '']
# c = [x for x in c if x != '']
#
#
# # Initiate dictionary generation function
# def make_dict(list):
#     global table
#     i = -1
#
#     # iterate through char array
#     while i < len(list) - 1:
#         i += 1
#         indicator = list[i][0]
#         ch = list[i][2]
#
#         # 1) CORRECT - if original and converted chars match (successfully recognized)
#         if indicator == " ":
#             chdict = table.get(ch, {})
#             chdict[ch] = chdict.get(ch, 0) + 1
#             table[ch] = chdict
#             continue
#
#         # 2) SUBSTITUTED - if char is not the last character and +/- follows -/+
#         if i + 1 < len(list):
#
#             # adjacent character and its indicator
#             ch1_ind = list[i + 1][0]
#             ch1 = list[i + 1][2]
#
#             # (this letter was added first)
#             if (indicator == "+" and ch1_ind == "-"):
#                 chdict = table.get(ch1, {})
#                 chdict[ch] = chdict.get(ch, 0) + 1
#                 table[ch1] = chdict
#                 i += 1 # increment i and skip next char
#                 continue
#
#             # (this letter was deleted first)
#             if (indicator == "-" and ch1_ind == "+"):
#                 chdict = table.get(ch, {})
#                 chdict[ch1] = chdict.get(ch1, 0) + 1
#                 table[ch] = chdict
#                 i += 1 # increment i and skip next char
#                 continue
#
#         # 3) DELETED - if char is not followed by another indicator and this indicator is "-"
#         if indicator == "-":
#             chdict = table.get(ch, {})
#             chdict["Del"] = chdict.get("Del", 0) + 1
#             table[ch] = chdict
#
#         # 4) INSERTED - if char is not followed by another indicator and this indicator is "+"
#         elif indicator == "+":
#             chdict = table.get("Del", {})
#             chdict[ch] = chdict.get(ch, 0) + 1
#             table["Del"] = chdict
#
#         # 5) OTHER - pass any edge cases for now (never found so far)
#         else:
#             print("-- something weird going on ---", indicator, ch)
#             pass
#
#
# # Initiate and generate dictionary
# table = {}
# for ol, cl in zip(o,c):
#     n = dl.ndiff(ol, cl)
#     list = [i for i in n]
#     make_dict(list)
#
#
# # Quality check - print dictionary
# # print(table)
