import difflib as dl

import re
# 50 lines
# o = open("moby_dick-orig/moby_dick-orig-chunk-aa.txt", "r").read()
# c = open("moby_dick-orig/moby_dick-orig-chunk-aa-converted.txt", "r").read()

# 10 lines
# o = open("moby_dick-10/moby_dick-orig-chunk-ab.txt", "r").read()
# c = open("moby_dick-10/moby_dick-orig-chunk-ab-converted.txt", "r").read()

o = """
CHAPTER 1. Loomings.

Call me Ishmael. Some years ago—never mind how long precisely—having
little or no money in my purse, and nothing particular to interest me
on shore, I thought I would sail about a little and see the watery part
of the world. It is a way I have of driving off the spleen and
regulating the circulation. Whenever I find myself growing grim about
the mouth; whenever it is a damp, drizzly November in my soul; whenever
I find myself involuntarily pausing before coffin warehouses, and
bringing up the rear of every funeral I meet; and especially whenever
my hypos get such an upper hand of me, that it requires a strong moral
principle to prevent me from deliberately stepping into the street, and
methodically knocking people’s hats off—then, I account it high time to
get to sea as soon as I can. This is my substitute for pistol and ball.
With a philosophical flourish Cato throws himself upon his sword; I
quietly take to the ship. There is nothing surprising in this. If they
but knew it, almost all men in their degree, some time or other,
cherish very nearly the same feelings towards the ocean with me.

There now is your insular city of the Manhattoes, belted round by
wharves as Indian isles by coral reefs—commerce surrounds it with her
surf. Right and left, the streets take you waterward. Its extreme
downtown is the battery, where that noble mole is washed by waves, and
cooled by breezes, which a few hours previous were out of sight of
land. Look at the crowds of water-gazers there.

Circumambulate the city of a dreamy Sabbath afternoon. Go from Corlears
Hook to Coenties Slip, and from thence, by Whitehall, northward. What
do you see?—Posted like silent sentinels all around the town, stand
thousands upon thousands of mortal men fixed in ocean reveries. Some
leaning against the spiles; some seated upon the pier-heads; some
looking over the bulwarks of ships from China; some high aloft in the
rigging, as if striving to get a still better seaward peep. But these
are all landsmen; of week days pent up in lath and plaster—tied to
counters, nailed to benches, clinched to desks. How then is this? Are
the green fields gone? What do they here?

But look! here come more crowds, pacing straight for the water, and
seemingly bound for a dive. Strange! Nothing will content them but the
extremest limit of the land; loitering under the shady lee of yonder
warehouses will not suffice. No. They must get just as nigh the water
as they possibly can without falling in. And there they stand—miles of
them—leagues. Inlanders all, they come from lanes and alleys, streets
and avenues—north, east, south, and west. Yet here they all unite. Tell
me, does the magnetic virtue of the needles of the compasses of all
those ships attract them thither?

Once more. Say you are in the country; in some high land of lakes. Take
almost any path you please, and ten to one it carries you down in a
dale, and leaves you there by a pool in the stream. There is magic in
"""

c = """
CHAPTER 4, Loomings.

Call me Ishmael. Some years ago—never mind how jong precisely—having
litte or no money in my purse, and nothing articular to interest me

on shore, Hthought [would sail about alittle and see the watery part

ofthe world. itis a way Fhave of driving offthe spleen and

regulating the ciroulation. Whenever I ind myself growing grim about

the mouth; whenever itis a damp, drizzly November in my soul; whenever
Hind myself involuntarily pausing before coffin warehouses, and

‘bringing up the rear of every funeral F meet, and especially whenever

‘my hypos get such an upper hand of me, that it requires a strong moral
principle to prevent me from detiberaiely stepping into the street, and
methodically knocking people's hats off_then, t account i high time to
get to sea as soon as toan. This is my substitute for pistol and ball

With a philosophical flourish Cato throws himself upon his sword: {
quietly take to the ship. There is nothing surprising in this. they

‘ut knew i, almost all men in their degree, some time or other,

cherish very neatly the same feelings towards the ocean with me,

‘There now is your insular city ofthe Manhatioes, belted round by
wharves as lodian isles by coral reefe—commerce surrounds it with her
surf Right and tefl the streets take you waterward. is extreme

downtown is the battery, where that noble mole is washed by waves, and
cooled by breezes, which a few hours previous were out of sight of

tend, Look at the crowds of water-gazers there.

Circumambulate the city of a dreamy Sabbath afternoon. Go from Cortears
Hook to Coenties Slip, and from thenoe, by Whitehall, northward, What

do you see?—Posted like silent sentinels all around the town, stand
thousands upon thousands of mortal men fixed in ocean reveries. Some
teaning against the spiles; some seated upon the pler-heads; some
looking over the bulwarks of ships from China some high aloft in the
‘igging, as i'stiving to geta stil better seaward peep. But these

are ail landsmen; of week days pent up in fath and plaster—tied to
‘punters, nailed fo benches, clinched to desks. How then is this? Are

the green fields gone? What de they here?

But look! here come more crowds, pacing straight for the water, and
seemingly bound for a dive. Strange! Nothing wil content them but the
extremest limit of the land; foitering under the shady lee of yonder
warehouses will not suffice. No. They must get just as nigh the water
as they possibly can without faiting in. And there they stand—mites of
them leagues. Intanders al, they come froma ianes and alleys, streets
and avenues—notth, east, south and west. Yet here they all unite. Teli
‘me, does the magnetic virtue of the needies of the compasses of all
those ships attract them thither?

‘Once more. Say you are in the country; in some high land offakes. Take
‘almost any path you please, and ten to one it carries you down in a
dale, and leaves you there by a pool in the stream. There is magic in
"""


o = [x.strip() for x in o.split("\n")]
c = [x.strip() for x in c.split("\n")]
o = [x for x in o if x != '']
c = [x for x in c if x != '']

# print(o)
# print(c)

table = {}
for ol, cl in zip(o,c):
    n = dl.ndiff(ol, cl)
    list = [i for i in n]  # list comprehension (dict, tuple, set comprehension)
    print(cl)
    make_dict(list)
table



#------------------#

# construct initial dictionary with deletion option

# set the starting index to -1
i = -1

# iterate through char array
while i < len(list) - 1:
    i += 1
    indicator = list[i][0]
    ch = list[i][2]

    # if original and converted chars match (successfully recognized)
    if indicator == " ":
        chdict = table.get(ch, {})
        chdict[ch] = chdict.get(ch, 0) + 1
        table[ch] = chdict
        continue

    # if char is not the last character and +/- follows -/+ (substituted)
    if i + 1 < len(list):
        ch1_ind = list[i + 1][0]
        ch1 = list[i + 1][2]

        # if this indicator and the following indicator indicate substitution
        if (indicator == "+" and ch1_ind == "-"):
            chdict = table.get(ch1, {})
            chdict[ch] = chdict.get(ch, 0) + 1
            table[ch1] = chdict
            i += 1 # increment i and skip next char
            continue

        if (indicator == "-" and ch1_ind == "+"):
            print(ch, "replaced")
#             if list[i + 1][2] not in table[ch]:
#                 table[ch][list[i + 1][2]] = 0
#             table[ch][list[i + 1][2]] += 1
            chdict = table.get(ch, {})
            chdict[ch1] = chdict.get(ch1, 0) + 1
            table[ch] = chdict
            i += 1 # increment i and skip next char
            continue

    # if char is not followed by another indicator and is deleted
    if indicator == "-":
        print(ch, "deleted")
#         if "Del" not in table[ch]:
#                 table[ch]["Del"] = 0
#         table[ch]["Del"] += 1
        chdict = table.get(ch, {})
        chdict["Del"] = chdict.get("Del", 0) + 1
        table[ch] = chdict

    # if char is not followed by another indicator and is inserted
    elif indicator == "+":
        print(ch, "inserted")
#         if ch not in table["Del"]:
#                 table["Del"][ch] = 0
#         table["Del"][ch] += 1
        chdict = table.get("Del", {})
        chdict[ch] = chdict.get(ch, 0) + 1
        table["Del"] = chdict

    # pass any edge cases for now
    else:
        print("-- something weird going on ---", indicator, ch)
        pass

#table
