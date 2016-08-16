import numpy as np

import sortedcontainers

from src.main.BaseObjects.Vehicle import Vehicle
from src.main.BaseObjects.ListBase import ListBase
from src.main.BaseObjects.Parameters import Parameters
from src.main.Algorithms.CostFunction import Cost

# routes object will need a big overhaul
# need to only concern ourselves with the last vehicle added to

from src.main.BaseObjects.Customer import Customer

class Dispatch():
    def __init__(self, customers, depot):
        ''' Dispatch will organize the vehicles '''
        ''' And organize the customers '''
        assert type(customers) == list, "Must send *list* of customers"
        assert type(customers[0]) == Customer, "Must send list of *customers*"
        assert depot not in customers, "Depot must not be in customers list"
        
        self.customers = customers
        self.depot = depot
        self.visitedCustomers = [] 
        self.vehicles = []

        self.feasibleGraph = self.buildFeasibleGraph()
        self._onDeck = Vehicle(self.depot)
        
    def solutionStr(self):
        vehstr = "\n".join([str(v) + " \t" + str(v.customerHistory) for v in self.vehicles])
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
        nexts.append(self._onDeck)
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

        return fNextPairs

    def addCustomer(self, vehicle, customer):
        if(vehicle == self._onDeck):
            self._onDeck = Vehicle(self.depot)
            self.vehicles.append(vehicle)
        vehicle.serveCustomer(customer)

        # print("Removing {} from {}".format(customer, self.customers))
        self.customers.remove(customer)



