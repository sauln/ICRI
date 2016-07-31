import numpy as np

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
        
        def build(self, problemSet):
            self.params = problemSet
            self.customers = problemSet.customers
            self.distMatrix = self.buildDistMatrix(problemSet.customers)
            self.timeMatrix = self.buildTimeMatrix(problemSet.customers)

        def buildDistMatrix(self, customers):
            distance_matrix = np.empty([len(customers), len(customers)])
            
            def distEuclid(x,y):
                return np.sqrt((x.xcoord - y.xcoord)**2 + (x.ycoord - y.ycoord)**2)
        
            for i in range(len(customers)):
                for j in range(len(customers)):
                    distance_matrix[i,j] = distEuclid(customers[i], customers[j])
            return distance_matrix

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

