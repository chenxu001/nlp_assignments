import math, collections

class LaplaceBigramLanguageModel:

    def __init__(self, corpus):
        """Initialize your data structures in the constructor."""
        # TODO your code here
        self.laplace_unigram_counts = collections.defaultdict(lambda: 0) # one word dict
        self.laplace_bigram_counts = collections.defaultdict(lambda: 0) # two words dict
        self.same_pre = collections.defaultdict(lambda: []) # list of second word with same previous word
        self.train(corpus)

    def train(self, corpus):
        """ Takes a corpus and trains your language model. 
                Compute any counts or other corpus statistics in this function.
        """    
        # TODO your code here
        for sentence in corpus.corpus:
            for i in range(len(sentence.data)-1): # add word in sentence except the last one </s>
                pre_token = sentence.data[i].word
                la_token = sentence.data[i+1].word
                self.laplace_unigram_counts[pre_token] += 1
                self.laplace_bigram_counts[(pre_token, la_token)] += 1
                self.same_pre[pre_token].append(la_token)

    def score(self, sentence):
        """ Takes a list of strings as argument and returns the log-probability of the 
                sentence using your language model. Use whatever data you computed in train() here.
        """
        # TODO your code here
        score = 0.0
        pre_add_list = []        
        for i in range(len(sentence)-1):
            if self.laplace_bigram_counts[(sentence[i], sentence[i+1])] == 0:
                self.laplace_bigram_counts[(sentence[i], sentence[i+1])] += 1
                self.laplace_unigram_counts[sentence[i]] += 1
                pre_add_list.append(sentence[i])
        
        for i in set(pre_add_list):
            self.laplace_unigram_counts[i] += len(set(self.same_pre[i]))
            for j in set(self.same_pre[i]):
                self.laplace_bigram_counts[(i, j)] += 1
                
        for i in range(len(sentence)-1):
            score += math.log(self.laplace_bigram_counts[(sentence[i], sentence[i+1])])
            score -= math.log(self.laplace_unigram_counts[sentence[i]])
                
        return score
