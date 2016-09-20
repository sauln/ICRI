import numpy as np

from sortedcontainers import SortedListWithKey 

from .Vehicle import Vehicle
from .Parameters import Parameters
from .Customer import Customer
from .CostFunction import Cost

#import Vehicle
#import Parameters
#import Customer
#import Cost



class Dispatch():
    def __init__(self, customers, depot=None):
        ''' Dispatch will organize the vehicles '''
        ''' And organize the customers '''
        if isinstance(customers, self.__class__):
            # copying from other dispatch
            dispatch = customers
            self.customers = list(dispatch.customers)
            self.depot = dispatch.depot
            self.visitedCustomers = list(dispatch.visitedCustomers)
            self.vehicles = [Vehicle(v) for v in dispatch.vehicles]
            self.feasibleGraph = dispatch.feasibleGraph
            self.delta = dispatch.delta
        else:
            self.customers = customers
            self.depot = depot
            self.visitedCustomers = [] 
            self.vehicles = []
            self.feasibleGraph = self.buildFeasibleGraph()

            self.delta = [1]*5
    
    def set_delta(self, delta):
        self.delta = delta

    def finish(self):
        for vehicle in self.vehicles:
            vehicle.serveCustomer(self.depot)

    def _onDeck(self):
        return Vehicle(self.depot)

    def solutionStr(self):
        vehstr = "\n".join([str(v) for v in self.vehicles])
        return "Vehicles: {} => \n{} ".format(len(self.vehicles), vehstr)


    ##############################################################
    #####     These should probably not be there
    def dist(self, a,b):
        # all of the cost objects should be dynamics
        return np.sqrt((a.x-b.x)**2 + (a.y-b.y)**2)

    def cost(self, start, c):
        # travel dist, measure of how much time remaining.
        return self.dist(start,c) + (c.end)

    ##############################################################

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

    def getNextVehicles(self):
        nexts = [vehicle for vehicle in self.vehicles]
        nexts.append(self._onDeck())
        return nexts

    def getFeasibles(self, vehicles):
        # usually only needs 1 of these, if that's the case,
        # we can do this in O(n) time instead of O(n*log(n)).
        nextPairs = [(vehicle, self.feasibleGraph[vehicle.lastCustomer]) \
            for vehicle in vehicles]
      
        # This is broken out to get better profile information
        # `customer in self.customers` takes a lot of time.
        # `
        fNextPairs = []
        for vehicle, cs in nextPairs:
            for customer in cs:
                if vehicle.isFeasible(customer) and customer in self.customers:
                    cost = Cost.gnnh(self.delta, vehicle, customer)
                    fNextPairs.append( (vehicle, customer, cost))
        
        #fNextPairs = [(vehicle, customer, Cost.gnnh(self.delta, vehicle, customer)) \
        #                for vehicle, cs in nextPairs \
        #                for customer in cs \
        #                if vehicle.isFeasible(customer) and customer in self.customers]
        
        cs = SortedListWithKey(key = lambda x: x[2])
        cs.update(fNextPairs)

        return cs 

    def addCustomer(self, vehicle, customer):
        if vehicle not in self.vehicles:
            self.vehicles.append(vehicle)
        vehicle.serveCustomer(customer)

        self.customers.remove(customer)

