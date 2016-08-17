import numpy as np

from src.main.BaseObjects.Customer import Customer
#from src.main.BaseObjects.ListBase import ListBase
from src.main.BaseObjects.Parameters import Parameters

class Vehicle():
    def __init__(self, depot):
        # constructing with seed != depot is deprecated
        if isinstance(depot, self.__class__):
            self.__dict__ = depot.__dict__.copy()
            self.customerHistory = list(depot.customerHistory)
        else:
            self.totalDist, self.totalSlack = 0,0
            self.totalTime, self.curCapacity = 0,0 
            self.servedCustomers = 0

            self.maxCapacity = Parameters().params.capacity
            self.timeMatrix = Parameters().timeMatrix
            self.distMatrix = Parameters().distMatrix
            self.depot = Parameters().depot
            
            assert self.depot == depot
            self.customerHistory = [depot]
            self.lastCustomer = depot
        
    def __str__(self):
        return "Veh: {}{:<34} \tat {:g} last served {}".format(self.servedCustomers, \
            "["+", ".join(str(c.custNo) for c in self.customerHistory) +"]", \
            self.totalDist, \
            self.lastCustomer.custNo)
    def __repr__(self):
        return self.__str__()

    def last(self):
        return self.lastCustomer

    def serveCustomer(self, customer):
        arrivalTime = self.totalTime + self.travelTime(customer)
        servedTime = max(arrivalTime, customer.readyTime)
        self.totalSlack += servedTime - arrivalTime
        self.totalTime = servedTime + customer.serviceLen
        self.totalDist += self.travelDist(customer)
        self.curCapacity += customer.demand
        self.customerHistory.append(customer)
        self.servedCustomers += 1
        self.lastCustomer = customer

    def isNotFull(self, end):
        return self.maxCapacity >= end.demand + self.curCapacity
    
    def isValidTime(self, end):
        return self.totalTime + self.travelTime(end) <= end.dueDate
    
    def canMakeItHomeInTime(self, end):
        return end.dueDate + Parameters().travelTime(end, self.depot) <= self.depot.dueDate
    
    def isFeasible(self, end):
        return self.isValidTime(end) and \
               self.isNotFull(end) #and \
               #self.canMakeItHomeInTime(end)

    def travelDist(self, end):
        return Parameters().travelDist(self.last(), end) 

    def travelTime(self, end):
        return Parameters().travelTime(self.last(), end) 

    def geographicCenter(self):
        custs = set(self)
        coords = [[c.xcoord, c.ycoord] for c in custs]
        center = np.mean(coords, axis=0)
        return center

    def debugStr(self, item):
        return "\n\t\tItem {} is being added to \n\t\t{}; \n\t\t{}\n\
                totaltime: {}  travelTime:{:3g}  duedate:{}\n\
                maxCap: {}     demand:{}      curCap: {}"\
            .format(item, self, self.feasibilityStr(item), \
                    self.totalTime, self.travelTime(item), item.dueDate, \
                    self.maxCapacity, item.demand, self.curCapacity)
            
    def feasibilityStr(self, item):
        return "isFeasible:{} ".format(self.isFeasible(item)) +\
               "isNotFull:{} ".format(self.isNotFull(item)) +\
               "isValidTime:{} ".format(self.isValidTime(item)) +\
               "canMakeItHome:{} ".format(self.canMakeItHomeInTime(item))

