#! /usr/bin/env python3
import collections # contains useful function to order dictionary
import sys        # command line arguments
import re         # regular expression tools
import os         # checking if file exists

if len(sys.argv) is not 3:
    print("Correct usage: wordCountTest.py <input text file> <output file>")
    exit()
wordCount = {}
textFname = sys.argv[1]
outputFname = sys.argv[2]

#make sure text files exist
if not os.path.exists(textFname):
    print ("text file input %s doesn't exist! Exiting" % textFname)
    exit()

if not os.path.exists(outputFname):
    print ("wordCount output file %s doesn't exist! Exiting" % outputFname)
    exit()

with open(textFname, 'r') as inp:
    for line in inp:
        line = line.casefold() #makes all characters same case
        line = line.strip()
        words = re.split('[ \W,\t]', line) #matches any non-alphanumeric character, comma, or tab whitespace from the line

        for word in words:
            if word not in wordCount:
                wordCount[word]= 1
            else:
                wordCount[word]+= 1

sortedWords = collections.OrderedDict(sorted(wordCount.items())) #remembers the order items were inserted from wordCount

with open(outputFname, "w") as out:
    for i, (a,b) in enumerate(sortedWords.items()): #enumerates the items in sortedWords
        if i == 0:
            pass
        else:
            out.write('{0} {1}\n'.format(a,b)) #writes the enumerated items formatted
