import numpy as np

import sortedcontainers
from src.main.SolomonProblem import SolomonProblem
from src.main.Customer import Customer
from src.main.Vehicle import Vehicle

class Routes():
    def __init__(self, sp, start, depot = None):
        self.sp = sp
        self.vList = []

        if(depot):
            self.vList.append(Vehicle(sp, depot))
            self.depot = depot
        else:
            self.depot = start
        self.vList.append(Vehicle(sp, start))

    def cost(self):
        # keep track of this while building please
        total = sum(r.travelDistance() for r in self.vList)
        return total

    def pop(self, index = -1):
        return self.vList.pop(index) 

    def __getitem__(self, index):
        return self.vList[index]

    def __str__(self):
        return "Number of routes: {}\n{}".format(len(self.vList), self.vList)
    
    def __repr__(self):
        return self.__str__()

    """ Route building """
    def addNext(self, vehicle, end):
        if(vehicle[-1].custNo == 0): #the depot
            nv = Vehicle(self.sp, self.depot, end)
            self.vList.append(nv)
        else:
            vehicle.append(end)

    def __len__(self):
        return len(self.vList)

    def finish(self):
        if(len(self.vList[0]) == 1): # remove our place holder depot route
            self.vList.pop(0)

        for v in self.vList: # add depot to end of each route 
            v.append(self.depot)

    def getBestNode(self, cf, delta, customers):
        return self.getBestNNodes(cf, delta, customers, 1)[0]

    def getBestNNodes(self, cf, delta, customers, size):
        cs = sortedcontainers.SortedListWithKey(key=lambda x: x[2])
        
        # with lots of routes, this could become unreasonable
        # is there any faster way than to look at all of them?
        for vehicle in self.vList:
            feasible = [c for c in customers if vehicle.isFeasible(c)]
            for c in customers:
                if(vehicle.isFeasible(c)):
                    res = (vehicle, c, cf.run(delta, vehicle, c))  
                    cs.add(res)

        #print("Ranked options: {}".format(cs))
        return cs[:size]


