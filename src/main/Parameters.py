import numpy as np
from scipy.spatial.distance import pdist, squareform


class Parameters:
    class __Parameters:
        def __init__(self):
            self.customers = None
            self.distMatrix = None
            self.timeMatrix = None
            self.params = None
        
        def __getattr__(self, name):
            return getattr(self.params, name)

        def __str__(self):
            return str(self.params) + str(self.distMatrix) + str(self.timeMatrix)
        
        def build(self, problemSet, topNodes, searchDepth, depot = None):
            self.depot, self.customers = (depot, problemSet.customers)\
                if depot is not None else (problemSet.customers[0], problemSet.customers[1:])

            self.params = problemSet
            self.distMatrix = self.buildDistMatrix(problemSet.customers)
            self.timeMatrix = self.buildTimeMatrix(problemSet.customers)
            self.topNodes = topNodes
            self.searchDepth = searchDepth

        def buildDistMatrix(self, customers):
            coords = np.asarray([[c.xcoord, c.ycoord] for c in customers]) 
            distm = squareform(pdist(coords, 'euclidean'))
            return distm 

        def buildTimeMatrix(self, customers):
            return self.distMatrix

    instance = None
    def __new__(cls):
        if not Parameters.instance:
            Parameters.instance = Parameters.__Parameters()
        return Parameters.instance
    def __getattr__(self, name):
        return getattr(self.instance, name)
    def __setattr(self, name):
        return setattr(self.instance, name)

