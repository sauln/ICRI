import numpy as np

import sortedcontainers

from src.main.Vehicle import Vehicle
from src.main.ListBase import ListBase
from src.main.Parameters import Parameters

class Routes(ListBase):
    def __init__(self, start, depot = None):
        super(Routes, self).__init__()
        if(depot):
            self.objList.append(Vehicle(depot))
            self.depot = depot
        else:
            self.depot = start
        self.objList.append(Vehicle(start))

    def cost(self):
        # keep track of this while building please
        total = sum(r.totalTravelDistance() for r in self.objList)
        return total

    def __str__(self):
        return "Routes: " + super().__str__() 
    
    def __repr__(self):
        return self.__str__()

    """ Route building """
    def addNext(self, vehicle, end):
        if(vehicle[-1].custNo == 0): #the depot
            nv = Vehicle(self.depot, end)
            self.objList.append(nv)
        else:
            vehicle.append(end)

    # every route ends at the depot, and the vehicle on deck is removed
    def finish(self):

        if(len(self.objList[0]) == 1): # remove our place holder depot route
            self.objList.pop(0)

        for v in self.objList: # add depot to end of each route 
            v.append(self.depot)

    def getBestNode(self, cf, delta, customers):
        return self.getBestNNodes(cf, delta, customers, 1)[0]

    def getBestNNodes(self, cf, delta, customers, size):
        cs = sortedcontainers.SortedListWithKey(key=lambda x: x[2])
        
        # with lots of routes, this could become unreasonable
        # is there any faster way than to look at all of them?
        for vehicle in self.objList:
            feasible = [c for c in customers if vehicle.isFeasible(c)]
            for c in customers:
                if(vehicle.isFeasible(c)):
                    res = (vehicle, c, cf.run(delta, vehicle, c))  
                    cs.add(res)

        #print("Ranked options: {}".format(cs))
        return cs[:size]


