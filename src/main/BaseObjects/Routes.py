import numpy as np

import sortedcontainers

from src.main.BaseObjects.Vehicle import Vehicle
from src.main.BaseObjects.ListBase import ListBase
from src.main.BaseObjects.Parameters import Parameters

# routes object will need a big overhaul
# need to only concern ourselves with the last vehicle added to

from src.main.BaseObjects.Customer import Customer

class Dispatch():
    def __init__(self, customers, depot):
        ''' Dispatch will organize the vehicles '''
        ''' And organize the customers '''
        self.vehicles = []

        assert type(customers) == list, "Must send *list* of customers"
        assert type(customers[0]) == Customer, "Must send list of *customers*"
        assert depot not in customers, "Depot must not be in customers list"
        
        self.customers = customers
        self.depot = depot
        self.visitedCustomers = [] 
        self.feasibleGraph = self.buildFeasibleGraph()

    #def findNextNodes(self):
    #    for vehicle in self.vehicles:

    def dist(self, a,b):
        # all of the cost objects should be dynamics
        return np.sqrt((a.x-b.x)**2 + (a.y-b.y)**2)

    def cost(self, start, c):
        # travel dist, measure of how much time remaining.
        return self.dist(start,c) + (c.end)

    def isFeasible(self, a, b):
        return a.readyTime + self.dist(a.location, b.location) <= b.dueDate

    def feasibleList(self, customer):
        return [c for c in self.customers  if self.isFeasible(customer, c) 
            and c is not customer]
    
    def buildFeasibleGraph(self):
        graph = {}
        for customer in self.customers:
            graph[customer] = self.feasibleList(customer)
        graph[self.depot] = self.feasibleList(self.depot)
        return graph

    def getRootNodes(self):
        nexts = [vehicle.lastServed for vehicle in self.vehicles]
        nexts.append(self.depot)
        return nexts




class Routes(ListBase):
    def __init__(self, start, depot = None):
        #this constructor should take a vehicle 
        super(Routes, self).__init__()
        if(depot):
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
            if(v[-1] != self.depot):
                v.update(self.depot)
                v.append(self.depot)
    
    #def cost(self):
    #    print("Need to find the cost")
    #    total = sum(r.totalDist for r in self.objList)
    #    return total

#if __name__ == "__main__":





