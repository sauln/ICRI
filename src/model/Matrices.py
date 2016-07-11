# -*- coding: utf-8 -*-
import os
import pickle
import numpy as np

from src.model.SolomonProblem import Customer, SolomonProblem

class Matrices():
    def __init__(self, customers):
        self.distMatrix = self.build_distMatrix(customers)
        self.timeMatrix = self.build_timeMatrix(customers)

    def distEuclid(self, x,y):
        return np.sqrt((x.xcoord - y.xcoord)**2 + (x.ycoord - y.ycoord)**2)

    def build_distMatrix(self, customers):
        distance_matrix = np.empty([len(customers), len(customers)])

        # there were some basic matrix multiplications that did this, werent' there?
        for i in range(len(customers)):
            for j in range(len(customers)):
                distance_matrix[i,j] = self.distEuclid(customers[i], customers[j])

        return distance_matrix

    def build_timeMatrix(self, customers):
        return self.distMatrix
        
    def __eq__(self, other):
        return np.array_equal(self.distMatrix, other.distMatrix) and \
               np.array_equal(self.timeMatrix, other.timeMatrix)

    def __str__(self):
        return "Shape: {}\nDistMatrix: {}".format(self.distMatrix.shape, self.distMatrix)

    def __repr__(self):
        return self.__str__()


def buildMatricesFromCustomerFile(input_filepath):
    with open(input_filepath, "rb") as f:
        problem = pickle.load(f)
        customers = problem.customers

    dmat = Matrices(customers)
    return dmat

