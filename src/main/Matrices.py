# -*- coding: utf-8 -*-
import os
import pickle
import numpy as np

# singleton matrices class
class Matrices:
    class __Matrices:
        def __init__(self):
            self.distMatrix = None
            self.timeMatrix = None
        
        def __str__(self):
            return repr(self) + str(self.distMatrix) + str(self.timeMatrix)
        
        def distEuclid(self, x,y):
            return np.sqrt((x.xcoord - y.xcoord)**2 + (x.ycoord - y.ycoord)**2)
        
        def build(self, customers):
            self.distMatrix = self.buildDistMatrix(customers)
            self.timeMatrix = self.buildTimeMatrix(customers)
        
        def buildDistMatrix(self, customers):
            distance_matrix = np.empty([len(customers), len(customers)])
            # there were some basic matrix multiplications that did this, werent' there?
            for i in range(len(customers)):
                for j in range(len(customers)):
                    distance_matrix[i,j] = self.distEuclid(customers[i], customers[j])
            return distance_matrix

        def buildTimeMatrix(self, customers):
            return self.distMatrix

    # functions to handle singleton aspects
    instance = None
    def __new__(cls):
        if not Matrices.instance:
            Matrices.instance = Matrices.__Matrices()
        return Matrices.instance
    def __getattr__(self, name):
        return getattr(self.instance, name)
    def __setattr__(self, name):
        return setattr(self.instance, name)

def buildMatricesFromCustomerFile(input_filepath):
    with open(input_filepath, "rb") as f:
        problem = pickle.load(f)
        customers = problem.customers

    dmat = Matrices(customers)

