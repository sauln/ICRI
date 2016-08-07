import numpy as np

import sortedcontainers

from src.main.Vehicle import Vehicle
from src.main.ListBase import ListBase
from src.main.Parameters import Parameters

# routes object will need a big overhaul
# need to only concern ourselves with the last vehicle added to


class Routes(ListBase):
    def __init__(self, start, depot = None):
        #this constructor should take a vehicle 
        super(Routes, self).__init__()
        if(depot):
            #self.objList.append(Vehicle(depot))
            self.depot = depot
        else:
            self.depot = start
        self.objList.append(Vehicle(start))

    def __str__(self):
        return "Total vehicles:{}\n".format(len(self)) \
            + "\n".join([repr(r) for r in self.objList])
   
    def __eq__(self, other):
        return self.objList == other.objList

    def __repr__(self):
        return self.__str__()

    """ Route building """
    def addNext(self, vehicle, end):
        if vehicle not in self:
            self.objList.append(vehicle)
        vehicle.append(end)

    def finish(self):
        # every route ends at the depot, and the vehicle on deck is removed
        #if(len(self[0]) == 1): self.pop(0)
        for v in self.objList:
            v.update(self.depot)
            v.append(self.depot)
    
    #def getBestNode(self, cf, delta, customers):
    #    return cf.getBestNode(delta, customers, self.last())

    #def lowestCostNext(self, cf, vehicle, delta, customers, size):
    #    return cf.lowestCostNext(vehicle, delta, customers, size)
   
    '''
    def getBestNNodes(self, cf, delta, customers, size):
        cstest = sortedcontainers.SortedListWithKey(key=lambda x: x[2])
        for c in customers:
            tmpList = []
            for vehicle in self:
                if(vehicle.isFeasible(c)): 
                    tmpList.append((vehicle, c, cf.run(delta,vehicle,c)))

            if tmpList:
                for res in tmpList:
                    cstest.add(res)
            else:
                t = Vehicle(self.depot)
                cstest.add((t, c, cf.run(delta, t, c)))

        return cstest[:size]
    '''

    def cost(self):
        total = sum(r.totalDist for r in self.objList)
        return total

