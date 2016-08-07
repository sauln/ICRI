import numpy as np


from src.main.BaseObjects.Customer import Customer
from src.main.BaseObjects.ListBase import ListBase
from src.main.BaseObjects.Parameters import Parameters

class Vehicle(ListBase):
    def __init__(self, *seed):
        super(Vehicle, self).__init__()
        self.totalDist, self.totalSlack = 0,0
        self.totalTime, self.curCapacity = 0,0 
        
        self.maxCapacity = Parameters().params.capacity
        self.timeMatrix = Parameters().timeMatrix
        self.distMatrix = Parameters().distMatrix
        self.depot = Parameters().depot

        for s in seed:
            self.append(s)

    def __eq__(self, other):
        return self.objList == other.objList
    def __str__(self):
        return super(Vehicle, self).__str__()+"t:{}".format(self.totalTime)

    def isNotFull(self, end):
        return self.maxCapacity >= end.demand + self.curCapacity
    def isValidTime(self, end):
        return self.totalTime + self.travelTime(end) <= end.dueDate
    def canMakeItHomeInTime(self, end):
        return end.dueDate + Parameters().travelTime(end, self.depot) <= self.depot.dueDate
    def isFeasible(self, end):
        return self.isValidTime(end) and \
               self.isNotFull(end) and \
               self.canMakeItHomeInTime(end)

    def travelDist(self, end):
        return Parameters().travelDist(self.last(), end) 

    def travelTime(self, end):
        return Parameters().travelTime(self.last(), end) 

    def geographicCenter(self):
        custs = set(self)
        coords = [[c.xcoord, c.ycoord] for c in custs]
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
    
    def firstItemUpdate(self, item):
        self.totalTime = (item.readyTime if item.custNo == 0 else item.dueDate) \
            + item.serviceLen
        self.curCapacity = item.demand

    def debugStr(self, item):
        return "Item {} is being added to {}; \nfull? {}, validTime? {}\n\
            totaltime: {}  travelTime:{}  duedate:{}\n\
            maxCap: {}     demand:{}      curCap: {}"\
            .format(item, self, self.isNotFull(item), self.isValidTime(item), \
                    self.totalTime, self.travelTime(item), item.dueDate, \
                    self.maxCapacity, item.demand, self.curCapacity)
            
    def feasibilityStr(self, item):
        return "isFeasible:{}".format(self.isFeasible(item)) +\
               "isNotFull:{}".format(self.isNotFull(item)) +\
               "isValidTime:{}".format(self.isValidTime(item)) +\
               "canMakeItHome:{}".format(self.canMakeItHomeInTime(item))

    def append(self, item):
        assert type(item) == Customer, "Cannot add type {} to route".format(type(value))
        
        if (self.__len__() == 0):
            self.firstItemUpdate(item)
        elif (item.custNo != 0):
            assert self.isFeasible(item), self.debugStr(item)           
            self.update(item)
        self.objList.append(item)



