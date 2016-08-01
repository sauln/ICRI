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

    def __str__(self):
        return "Routes: " + super().__str__() 
    
    def __repr__(self):
        return self.__str__()

    """ Route building """
    def addNext(self, vehicle, end):
        if(vehicle.last().custNo == 0): #the depot
            nv = Vehicle(self.depot, end)
            self.objList.append(nv)
        else:
            vehicle.append(end)

    def finish(self):
        # every route ends at the depot, and the vehicle on deck is removed
        if(len(self[0]) == 1): self.pop(0)
        for v in self.objList:
            v.update(self.depot)
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
                    cs.add((vehicle, c, cf.run(delta, vehicle, c)))

        return cs[:size]

    def cost(self):
        total = sum(r.totalDist for r in self.objList)
        return total

