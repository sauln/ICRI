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

class Customer():
    #todo: change these to camel case
    def __init__(self, custNo, xcoord, ycoord, demand, readyTime, dueDate, serviceLen):
        self.custNo       = custNo
        self.xcoord       = xcoord
        self.ycoord       = ycoord
        self.demand       = demand
        self.readyTime    = readyTime
        self.dueDate      = dueDate
        self.serviceLen   = serviceLen

        self._serviceTime = 0 # time this customer was serviced
        self._arrivalTime = 0 # time route arrived at this customer

    def serviceTime(self):
        #the actual time a customer was serviced
        return max(self._arrivalTime, self.readyTime)

    def setArrivalTime(self, prev):
        # use the actual timeTravel matrix 
        travelTime = np.sqrt(\
            (prev.xcoord - self.xcoord)**2 + (prev.ycoord - self.ycoord)**2)

        self._arrivalTime = prev.serviceTime() + prev.serviceLen + travelTime

    def __str__(self):
        return "ID: {:3}({}) t.({:3},{:3})+{}".\
            format(self.custNo, self.demand, \
                   self.readyTime, self.dueDate, self.serviceLen)

    def __repr__(self):
        return "{}".format(self.custNo)

    def __eq__(self, other):
        return self.custNo == other.custNo and \
               self.xcoord  == other.xcoord  and \
               self.ycoord  == other.ycoord  and \
               self.demand  == other.demand  and \
               self.readyTime == other.readyTime and \
               self.dueDate == other.dueDate and \
               self.serviceLen == other.serviceLen

