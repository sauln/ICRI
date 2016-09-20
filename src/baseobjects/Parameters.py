import numpy as np
from scipy.spatial.distance import pdist, squareform

class Parameters:
    class __Parameters:
        def __init__(self):
            #self.customers = None
            self.distMatrix = None
            self.timeMatrix = None
            self.params = None
            self.depot = None

        def __getattr__(self, name):
            return getattr(self.params, name)

        def __str__(self):
            return str(self.params) + str(self.distMatrix) + str(self.timeMatrix)
        
        def build(self, problemSet, topNodes, searchDepth, depot = None):
            if depot is not None: 
                self.depot = depot
                #self.customers = problemSet.customers
            else:
                self.depot = problemSet.customers[0]
                #self.customers = problemSet.customers[1:]

            self.params = problemSet
            self.distMatrix = self.buildDistMatrix(problemSet.customers)
            self.timeMatrix = self.buildTimeMatrix(problemSet.customers)
            self.topNodes = topNodes
            self.searchDepth = searchDepth

        #def getCustomers(self):
        #    return list(self.customers)

        def buildDistMatrix(self, customers):
            coords = np.asarray([[c.location.x, c.location.y] for c in customers]) 
            distm = squareform(pdist(coords, 'euclidean'))
            return distm 

        def buildTimeMatrix(self, customers):
            return self.distMatrix

        def travelTime(self, start, end):
            return self.timeMatrix[start.custNo, end.custNo]

        def travelDist(self, start, end):
            return self.distMatrix[start.custNo, end.custNo]

    instance = None
    def __new__(cls):
        if not Parameters.instance:
            Parameters.instance = Parameters.__Parameters()
        return Parameters.instance
    def __getattr__(self, name):
        return getattr(self.instance, name)
    def __setattr(self, name):
        return setattr(self.instance, name)
    


