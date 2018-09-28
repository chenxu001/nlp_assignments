#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 18:46:32 2018

@author: chen
"""

"""
Viterbi algorithms, trigram hmm
according to: http://www.cs.columbia.edu/~mcollins/hmms-spring2013.pdf
"""

import sys
from collections import defaultdict
from simple_gene_tagger import emission_prob
import math
import numpy as np

def probability(state_counts_file):
    two_gram = defaultdict(lambda: 0)
    prob = defaultdict(lambda: 0)
    lines = state_counts_file.readlines()
    for l in lines:
        line = l.strip('\n').split()
        if line[1] == '2-GRAM':
            two_gram[(line[2], line[3])] += int(line[0])
        if line[1] == '3-GRAM':
            prob[(line[2], line[3], line[4])] += int(line[0]) # counts of 3-gram
    for i in prob:
        prob[i] /= two_gram[(i[0], i[1])]
    state_counts_file.seek(0)
    emis_prob = emission_prob(state_counts_file)
    for i in emis_prob:
        prob[i] = emis_prob[i] # add emission probability
    
    return prob

def viterbi(sentence, tag_list, prob):
    if sentence == []:
        return
    
    pro_matrix = np.full((len(sentence), len(tag_list), len(tag_list)), -np.inf)
    trace_matrix = np.zeros((len(sentence), len(tag_list), len(tag_list)))

    for word in sentence:
        i = 0
        while (i < len(tag_list) and prob[(word, tag_list[i])] == 0):
            i += 1
        if i == len(tag_list):
            for tag in tag_list:
                prob[(word, tag)] = prob[('_RARE_', tag)]
                
    for j in range(len(tag_list)):
        if prob[('*', '*', tag_list[j])] == 0 or prob[(sentence[0], tag_list[j])] == 0:
            continue
        pro_matrix[0][j][j] = 0
        pro_matrix[0][j][j] += math.log(prob[('*', '*', tag_list[j])])
        pro_matrix[0][j][j] += math.log(prob[(sentence[0], tag_list[j])])
    
    for i in range(len(tag_list)):
        for j in range(len(tag_list)):
            if pro_matrix[0][i][i] == -np.inf or prob[('*', tag_list[i], tag_list[j])] == 0 \
            or prob[(sentence[1], tag_list[j])] == 0:
                continue
            pro_matrix[1][i][j] = pro_matrix[0][i][i]
            pro_matrix[1][i][j] += math.log(prob[('*', tag_list[i], tag_list[j])])
            pro_matrix[1][i][j] += math.log(prob[(sentence[1], tag_list[j])])

    for w in range(2, len(sentence)):
        for k in range(len(tag_list)):
            for i in range(len(tag_list)):
                for j in range(len(tag_list)):
                    if pro_matrix[w-1][k][i] == -np.inf or \
                    prob[(tag_list[k], tag_list[i], tag_list[j])] == 0 or \
                    prob[(sentence[w], tag_list[j])] == 0:
                        continue
                    prob_tmp = pro_matrix[w-1][k][i]
                    prob_tmp += math.log(prob[(tag_list[k], tag_list[i], tag_list[j])])
                    prob_tmp += math.log(prob[(sentence[w], tag_list[j])])
                    if prob_tmp > pro_matrix[w][i][j]:
                        pro_matrix[w][i][j] = prob_tmp
                        trace_matrix[w][i][j] = k

    prob_max = pro_matrix[-1][0][0] + math.log(prob[(tag_list[0], tag_list[0], 'STOP')])
    tag_n = 0
    tag_n_1 = 0
    for i in range(len(tag_list)):
        for j in range(len(tag_list)):
            if prob[(tag_list[i], tag_list[j], 'STOP')] == 0:
                continue
            prob_tmp = pro_matrix[-1][i][j] + math.log(prob[(tag_list[i], tag_list[j], 'STOP')])
            if prob_max < prob_tmp:
                prob_max = prob_tmp
                tag_n = j
                tag_n_1 = i
    
    reverse_tag_index = [tag_n, tag_n_1]
    for i in range(len(sentence)-3, -1, -1):
        index_1 = int(reverse_tag_index[-1])
        index_2 = int(reverse_tag_index[-2])
        reverse_tag_index.append(trace_matrix[i+2][index_1][index_2])
    reverse_tag_index.reverse()
    final_tag = []
    for i in reverse_tag_index:
        final_tag.append(tag_list[int(i)])
        
    return final_tag

def hmm_gene_tag(corpus_file, counts_file, output):
    prob = probability(counts_file)
    tag_list = ['I-GENE', 'O']
    sentence = []
    for l in corpus_file.readlines():
        line = l.strip('\n')
        if line:
            sentence.append(line)
        else:
            final_tag = viterbi(sentence, tag_list, prob)
            for i in range(len(sentence)):
                output.write("%s %s\n" % (sentence[i], final_tag[i]))
            output.write("%s\n" % line)
            sentence = []
            
if __name__ == '__main__':
    
    counts_file = open(sys.argv[1], 'r')
    file_to_tag = open(sys.argv[2], 'r')
    
    hmm_gene_tag(file_to_tag, counts_file, sys.stdout)
        
    