import numpy as np


from src.main.Customer import Customer
from src.main.ListBase import ListBase
from src.main.Parameters import Parameters

class Vehicle(ListBase):
    def __init__(self, *seed):
        super(Vehicle, self).__init__()
        self.curCapacity, self.totalDist, self.totalSlack, self.totalTime = 0,0,0,0
        self.depot = seed[0]
        self.maxCapacity = Parameters().params.capacity
        self.timeMatrix = Parameters().timeMatrix
        self.distMatrix = Parameters().distMatrix

        self.curCapacity = 0
        for s in seed:
            self.append(s)

    def isNotFull(self, end):
        return self.maxCapacity >= end.demand + self.curCapacity
    def isValidTime(self, end):
        return self.totalTime + self.travelTime(self.last(), end) <= end.dueDate
    def isFeasible(self, end):
        return (self.isValidTime(end) and self.isNotFull(end))
   
    def confirmEnds(self, start, end = None):
        if end is None:
            end = start
            start = self.last()
        return start, end 

    def travelDist(self, start, end = None):
        start, end = self.confirmEnds(start, end)
        return self.distMatrix[start.custNo, end.custNo]

    def travelTime(self, start, end = None):
        start, end = self.confirmEnds(start, end)
        return self.timeMatrix[start.custNo, end.custNo]
    
    def geographicCenter(self):
        coords = [[c.xcoord, c.ycoord] for c in self]
        center = np.mean(coords, axis=0)
        return center

    def update(self, item):
        assert self.last() != item, "Need to update values before inserting!"

        arrivalTime = self.totalTime + self.travelTime(item)
        srv = max(arrivalTime, item.readyTime)
        self.totalSlack  += srv - arrivalTime
        self.totalTime   =  srv + item.serviceLen
        self.totalDist   += self.travelDist(item)
        self.curCapacity += item.demand

    def append(self, item):
        assert type(item) == Customer, "Cannot add type {} to route".format(type(value))
        if(item.custNo is not 0 and self.__len__() != 0): #not depot and not first item
            assert self.isFeasible(item), "Item {} is not feasible".format(item)
            self.update(item)
        self.objList.append(item)

