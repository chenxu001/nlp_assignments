import math, collections
from LaplaceUnigramLanguageModel import LaplaceUnigramLanguageModel

class StupidBackoffLanguageModel:

    def __init__(self, corpus):
        """Initialize your data structures in the constructor."""
        # TODO your code here
        self.unigram_counts = collections.defaultdict(lambda: 0)
        self.bigram_counts = collections.defaultdict(lambda: 0)
        self.laplace_unigram_model = LaplaceUnigramLanguageModel(corpus)
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
                self.unigram_counts[pre_token] += 1
                self.bigram_counts[(pre_token, la_token)] += 1

    def score(self, sentence):
        """ Takes a list of strings as argument and returns the log-probability of the 
                sentence using your language model. Use whatever data you computed in train() here.
        """
        # TODO your code here
        laplace_unigram_score = self.laplace_unigram_model.score(sentence)
        score = 0
        for i in range(len(sentence)-1):
            if self.bigram_counts[(sentence[i], sentence[i+1])] == 0:
                score += math.log(0.4 * self.laplace_unigram_model.laplace_unigram_counts[sentence[i]])
                score -= math.log(self.laplace_unigram_model.total)
            else:
                score += math.log(self.bigram_counts[(sentence[i], sentence[i+1])])
                score -= math.log(self.unigram_counts[sentence[i]])
        return score
