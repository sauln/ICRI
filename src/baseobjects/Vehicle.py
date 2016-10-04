import numpy as np

from .Customer import Customer
from .Parameters import Parameters
#import Customer
#import Parameters

class Vehicle():
    def __init__(self, depot):
        # constructing with seed != depot is deprecated
        if isinstance(depot, self.__class__):
            vehicle = depot
            self.totalDist = vehicle.totalDist
            self.totalSlack = vehicle.totalSlack
            self.totalTime = vehicle.totalTime
            self.curCapacity = vehicle.curCapacity
            self.servedCustomers = vehicle.servedCustomers
            self.customerHistory = list(vehicle.customerHistory)
            self.lastCustomer = vehicle.lastCustomer
        else:
            self.totalDist, self.totalSlack = 0,0
            self.totalTime, self.curCapacity = 0,0 
            self.servedCustomers = 0
            
            self.customerHistory = [depot]
            self.lastCustomer = depot
        
        self.maxCapacity = Parameters().params.capacity
        self.timeMatrix = Parameters().timeMatrix
        self.distMatrix = Parameters().distMatrix
        self.depot = Parameters().depot
    
    def __hash__(self):
        return hash((str(self.customerHistory), self.totalDist, self.curCapacity))

    def __eq__(self, other):
        return other is not None and \
               self.customerHistory == other.customerHistory and \
               self.totalDist       == other.totalDist and \
               self.curCapacity     == other.curCapacity

    def __str__(self):
        return "Veh: {}{}".format(self.servedCustomers, \
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
        if customer.custNo is not 0:
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
        custs = set(self.customerHistory)
        custs.remove(Parameters().depot)
        coords = [[c.location.x, c.location.y] for c in custs]
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

