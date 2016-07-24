from src.main.Matrices import Matrices
import numpy as np

class SolomonProblem():
    def __init__(self, name, numVeh, capacity, customers):
        self.problemName     = name
        self.numVehicles     = numVeh
        self.capacity        = capacity
        self.customers       = customers

    def prepare(self):
        matrices = Matrices(self.customers)
        self.timeMatrix = matrices.timeMatrix
        self.distMatrix = matrices.distMatrix

    def __str__(self):
        return "{} Num Vehicles: {}  Capacity: {}  Num Customers: {}".\
            format(self.problemName,self.numVehicles,self.capacity,len(self.customers))

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return (self.problemName == other.problemName) and \
               (self.numVehicles == other.numVehicles) and \
               (self.capacity == other.capacity) and \
               (self.customers == other.customers)
