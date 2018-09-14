import math, collections

class LaplaceUnigramLanguageModel:

    def __init__(self, corpus):
        """Initialize your data structures in the constructor."""
        # TODO your code here
        self.laplace_unigram_counts = collections.defaultdict(lambda: 0)
        self.total = 0
        self.train(corpus)

    def train(self, corpus):
        """ Takes a corpus and trains your language model. 
                Compute any counts or other corpus statistics in this function.
        """    
        # TODO your code here
        for sentence in corpus.corpus:            
            for datum in sentence.data[1:-1]:
                token = datum.word
                self.laplace_unigram_counts[token] += 1
                self.total += 1

    def score(self, sentence):
        """ Takes a list of strings as argument and returns the log-probability of the 
                sentence using your language model. Use whatever data you computed in train() here.
        """
        # TODO your code here
        score = 0.0
        number_of_unseen = 0
        for token in sentence[1:-1]:
            if self.laplace_unigram_counts[token] == 0:
                number_of_unseen += 1
        if number_of_unseen > 0:
            for t in self.laplace_unigram_counts:
                self.laplace_unigram_counts[t] += 1
            self.total += len(self.laplace_unigram_counts)            
        for token in sentence[1:-1]:
            count = self.laplace_unigram_counts[token]
            score += math.log(count)
            score -= math.log(self.total)
        return score
