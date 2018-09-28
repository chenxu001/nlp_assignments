#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 10:34:41 2018

@author: chen
"""

"""
baseline, a simple gene tagger: y = argmax p(x|y)
"""

import sys
from collections import defaultdict

def emission_prob(gene_counts_file):
    total_counts = defaultdict(lambda: 0)
    lines = gene_counts_file.readlines()
    for l in lines:
        line = l.strip('\n').split()
        if line[1] == 'WORDTAG':
            total_counts[line[2]] += int(line[0])

    emis_prob = defaultdict(lambda: 0)
    for l in lines:
        line = l.strip('\n').split()
        if line[1] == 'WORDTAG':
            emis_prob[(line[3], line[2])] = int(line[0]) / total_counts[line[2]]
    return emis_prob

def simple_gene_tag(corpus_file, emis_prob, output):
    for l in corpus_file.readlines():
        line = l.strip('\n')
        if line:
            if emis_prob[(line, 'I-GENE')] == 0 and emis_prob[(line, 'O')] == 0:
                for tag in ['I-GENE', 'O']:
                    emis_prob[(line, tag)] = emis_prob[('_RARE_', tag)]
            if emis_prob[(line, 'I-GENE')] > emis_prob[(line, 'O')]:
                final_tag = 'I-GENE'
            else:
                final_tag = 'O'
            output.write("%s %s\n" % (line, final_tag))
        else:
            output.write("%s\n" % line)
        
if __name__ == '__main__':
    
    counts_file = open(sys.argv[1], 'r')
    file_to_tag = open(sys.argv[2], 'r')
    
    e_prob = emission_prob(counts_file)
    simple_gene_tag(file_to_tag, e_prob, sys.stdout)
            