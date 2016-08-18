import numpy as np

from sortedcontainers import SortedListWithKey 

from src.main.BaseObjects.Vehicle import Vehicle
from src.main.BaseObjects.Parameters import Parameters
from src.main.Algorithms.CostFunction import Cost
from src.main.BaseObjects.Customer import Customer

class Dispatch():
    def __init__(self, customers, depot=None):
        ''' Dispatch will organize the vehicles '''
        ''' And organize the customers '''
        # assert type(customers) == list, "Must send *list* of customers"
        # assert type(customers[0]) == Customer, "Must send list of *customers*"
        # assert depot not in customers, "Depot must not be in customers list"
        if isinstance(customers, self.__class__):
            # copying from other dispatch
            dispatch = customers
            self.customers = list(dispatch.customers)
            self.depot = dispatch.depot
            self.visitedCustomers = list(dispatch.visitedCustomers)
            self.vehicles = [Vehicle(v) for v in dispatch.vehicles]
            #self.vehicles = list(dispatch.vehicles)
            self.feasibleGraph = dispatch.feasibleGraph
       
        else:
            self.customers = customers
            self.depot = depot
            self.visitedCustomers = [] 
            self.vehicles = []
            self.feasibleGraph = self.buildFeasibleGraph()
        #self._onDeck = Vehicle(self.depot)
       
    def _onDeck(self):
        return Vehicle(self.depot)

    def solutionStr(self):
        vehstr = "\n".join([str(v) for v in self.vehicles])
        return "Vehicles: {} => \n{} ".format(len(self.vehicles), vehstr)

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

    def getNextVehicles(self):
        nexts = [vehicle for vehicle in self.vehicles]
        nexts.append(self._onDeck())
        return nexts

    def getFeasibles(self, vehicles):
        # print("get maybe feasible customers per vehicle")
        nextPairs = [(vehicle, self.feasibleGraph[vehicle.lastCustomer]) \
            for vehicle in vehicles]
        
        # print("Flatten customers and get costs if feasible")
        fNextPairs = [(vehicle, customer, Cost.gnnh([1]* 7, vehicle, customer)) \
                        for vehicle, cs in nextPairs \
                        for customer in cs \
                        if vehicle.isFeasible(customer) and customer in self.customers]
        
        cs = SortedListWithKey(key = lambda x: x[2])
        cs.update(fNextPairs)

        return cs 

    def addCustomer(self, vehicle, customer):
        if vehicle not in self.vehicles:
            self.vehicles.append(vehicle)
        vehicle.serveCustomer(customer)

        # print("Removing {} from {}".format(customer, self.customers))
        self.customers.remove(customer)

