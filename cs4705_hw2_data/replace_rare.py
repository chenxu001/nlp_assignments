#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  6 15:48:36 2018

@author: chen
"""

import sys, json
import collections

word_c = collections.defaultdict(lambda: 0)
def word_count(counts_file):
    f = open(counts_file)
    for l in f.readlines():
        line = l.strip().split(' ')
        if line[1] == 'UNARYRULE':
            word_c[line[3]] += int(line[0])

def replace_rare(tree): 
    if isinstance(tree, str): return        
    if len(tree) == 3:
        replace_rare(tree[1])
        replace_rare(tree[2])
    elif len(tree) == 2:
        if word_c[tree[1]] < 5:
            tree[1] = '_RARE_'

def main(parse_file, output_file):
    out_file = open(output_file, 'w')
    for l in open(parse_file):
        t = json.loads(l)
        replace_rare(t)
        out_file.write(json.dumps(t) + '\n')
    out_file.close()

def usage():
        sys.stderr.write("""
        Usage: python replace_rare.py [tree_file] [output_file]
                Replace rare words with '_RARE_'\n""")

if __name__ == "__main__": 
    if len(sys.argv) != 3:
        usage()
        sys.exit(1)
    word_count('cfg.counts')
    main(sys.argv[1], sys.argv[2])

    