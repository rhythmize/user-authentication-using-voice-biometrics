import operator
import numpy as np
from sklearn.mixture import GaussianMixture as GMM

class GMMSet(object):

    def __init__(self, gmm_order = 32):
        self.gmms = []
        self.gmm_order = gmm_order
        self.y = []

    def fit_new(self, x, label):
        self.y.append(label)
        gmm = GMM(self.gmm_order)
        gmm.fit(x)
        self.gmms.append(gmm)

    def gmm_score(self, gmm, x):
        return np.sum(gmm.score(x))

    def before_pickle(self):
        pass

    def after_pickle(self):
        pass

    def predict_one(self, x):
        #print self.gmms
        scores = [self.gmm_score(gmm, x) / len(x) for gmm in self.gmms]
        #print "scores :\n",scores
        p = sorted(enumerate(scores), key=operator.itemgetter(1), reverse=True)
        #print "p :\n",p
        p = [(str(self.y[i]), y, p[0][1] - y) for i, y in p]
        #print "p :\n",p
        result = [(self.y[index], value) for (index, value) in enumerate(scores)]
        #print "result :\n",result
        p = max(result, key=operator.itemgetter(1))
        return p[0]
