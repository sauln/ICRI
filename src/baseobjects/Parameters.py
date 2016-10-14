import numpy as np
from scipy.spatial.distance import pdist, squareform

class Parameters:
    class __Parameters:
        def __init__(self):
            self.distMatrix = None
            self.timeMatrix = None
            self.params = None

        def __getattr__(self, name):
            return getattr(self.params, name)

        def __str__(self):
            return str(self.params) + str(self.distMatrix) + str(self.timeMatrix)
        
        def build(self, problemSet):
            self.depot = problemSet.customers[0]

            self.params = problemSet
            self.distMatrix = self.buildDistMatrix(problemSet.customers)
            self.timeMatrix = self.buildTimeMatrix(problemSet.customers)

        def buildDistMatrix(self, customers):
            coords = np.asarray([[c.location.x, c.location.y] for c in customers]) 
            distm = squareform(pdist(coords, 'euclidean'))
            return distm 

        def buildTimeMatrix(self, customers):
            return self.distMatrix

        def travel_time(self, start, end):
            return self.timeMatrix[start.custNo, end.custNo]

        def travel_dist(self, start, end):
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
    
