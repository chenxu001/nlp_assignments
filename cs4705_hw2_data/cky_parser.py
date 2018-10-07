#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 16:49:41 2018

@author: chen
"""
import sys, collections, json

count_x = {}
prob = collections.defaultdict(lambda: 0)
rules = {}
words_in_trainning = []

def compute_prob(counts_file):
    f = open(counts_file)
    lines = f.readlines()
    for l in lines:
        line = l.strip().split(' ')
        if line[1] == 'NONTERMINAL':
            count_x[line[2]] = int(line[0])
        elif line[1] == 'UNARYRULE':
            prob[(line[2], line[3])] = int(line[0])
            words_in_trainning.append(line[3])
        elif line[1] == 'BINARYRULE':
            prob[(line[2], line[3], line[4])] = int(line[0])
            rules.setdefault(line[2], [])
            rules[line[2]].append((line[3], line[4]))
    for item in prob:
        prob[item] /= count_x[item[0]]

class CkyParser:
    def __init__(self):
        self.bp = {}
        self.sentence = []
        
    def cky(self, sentence):
        self.sentence = sentence
        prob_of_tree = collections.defaultdict(lambda: 0)
        n = len(sentence)
        for i in range(1, n+1):
            word = sentence[i-1]
            if word not in words_in_trainning:
                word = '_RARE_'
            for x in count_x:
                prob_of_tree[(i, i, x)] = prob[(x, word)]
        
        for l in range(1, n):
            for i in range(1, n-l+1):
                j = i + l
                for x in rules:
                    prob_of_tree[(i, j, x)] = prob[(x, rules[x][0][0], rules[x][0][1])] \
                    * prob_of_tree[(i, i, rules[x][0][0])] * prob_of_tree[(i+1, j, rules[x][0][1])]
                    self.bp[(i, j, x)] = [rules[x][0], i]
                    for s in range(i, j):
                        for rule in rules[x]:
                            prob_tmp = prob[(x, rule[0], rule[1])] \
                            * prob_of_tree[(i, s, rule[0])] * prob_of_tree[(s+1, j, rule[1])]
                            if prob_of_tree[(i, j, x)] < prob_tmp:
                                prob_of_tree[(i, j, x)] = prob_tmp
                                self.bp[(i, j, x)] = [rule, s]

        top = 'S'                                                       
        if prob_of_tree[(1, n, top)] == 0:
            for x in rules:
                if prob_of_tree[(1, n, x)] > prob_of_tree[(1, n, top)]:
                    top = x
        
        return self.write_json(1, n, top)

    def write_json(self, i, j, top):
        if i == j:
            data = [top, self.sentence[i-1]]
        else:
            data = [top, self.write_json(i, self.bp[(i, j, top)][1], self.bp[(i, j, top)][0][0]), \
            self.write_json(self.bp[(i, j, top)][1]+1, j, self.bp[(i, j, top)][0][1])]
        return data

def main(corpus_file, output_file):
    f = open(corpus_file)
    out_file = open(output_file, 'w')
    lines = f.readlines()
    parser = CkyParser()
    for l in lines:
        line = l.strip().split(' ')
        data = parser.cky(line)
        d = json.dumps(data)
        out_file.write(d + '\n')
    out_file.close()
    
def usage():
    sys.stderr.write("""
        Usage: python cky_parser.py [corpus_file] [output_file]\n""")
        
if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage()
        sys.exit(1)
    compute_prob('cfg.counts_replace_rare')
    main(sys.argv[1], sys.argv[2])
    
        