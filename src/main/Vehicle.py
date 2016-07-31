from src.main.Customer import Customer

from src.main.ListBase import ListBase
from src.main.Parameters import Parameters

class Vehicle(ListBase):
    def __init__(self, *seed):
        super(Vehicle, self).__init__()
        self.curCapacity, self.distTravel, self.totalSlack, self.totalTime = 0,0,0,0
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
   
    def travelTime(self, start, end = None):
        if end is None:
            end = start
            start = self.last()
        return self.timeMatrix[start.custNo, end.custNo]
    
    def travelDist(self, start, end = None):
        if end is None:
            end = start
            start = self.last()
        return self.distMatrix[start.custNo, end.custNo]

    def totalTravelDistance(self):
        # meant to calc on the fly
        tot = 0
        for i in range(len(self)-1):
            tot += self.travelDist(self[i], self[i+1])
        return tot

    def geographicCenter(self):
        xs = [c.xcoord for c in self]
        ys = [c.ycoord for c in self]

        x, y = sum(xs)/len(xs), sum(ys)/len(ys)

        return (x, y)

    def lastCustomer(self):
        # should this be a better method of try/catch?
        return self.last()

    def update(self, item):
        arrivalTime = self.totalTime + self.travelTime(self.last(), item)
        srv = max(arrivalTime, item.readyTime)
        slackTime = srv - arrivalTime
        self.totalSlack += slackTime
        self.totalTime = srv + item.serviceLen
        self.curCapacity += item.demand

    def append(self, item):
        assert type(item) == Customer, "Cannot add type {} to route".format(type(value))
        if(item.custNo is not 0 and self.__len__() != 0): #not depot and not first item
            assert self.isFeasible(item), "Item {} is not feasible".format(item)
            self.update(item)
        self.objList.append(item)

