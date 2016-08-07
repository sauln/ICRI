import time
import sys
import sortedcontainers
from copy import copy, deepcopy

from src.main.Algorithms.Heuristic import Heuristic
from src.main.Algorithms.CostFunction import Cost
from src.main.Algorithms.NextFinder import NextFinder

from src.main.BaseObjects.Routes import Routes
from src.main.BaseObjects.Parameters import Parameters

class RollOut:
    def __init__(self):
        self.heuristic = Heuristic()
        pm = Parameters()
        self.depot = pm.depot
        self.workingCustomers = list(pm.customers)


        # need to maintain two routes objects
        self.routes = Routes(self.depot)
        self.bestSequence = Routes(self.depot)
        self.W = 100
        self.delta = [[10,1,1,1,1,1,1]]
        self.goldenRoutes = None
        
        
        # don't need 'start' because we can grab off end of list
        start = self.depot
        numVehicles = minNumVeh = lowestCost = float("inf") 
        lowerLimit = 12

    def constructRoute(self):
        lowestVehicle = self.bestSequence[-1]
        routes = self.rollOut()
        return routes 
   
    def rollOut(self):
        self.d = self.delta[0]        
        while len(self.workingCustomers) > 0: 
            self.rollOutNextCustomer() 
        self.goldenRoutes.finish()
        return self.goldenRoutes 

    def rollOutNextCustomer(self): 
        topCusts = NextFinder.getBestNNodes(self.d, self.bestSequence[-1],  \
                                                    self.workingCustomers,  5)

        lowestSeqObj = self.lowestProjectedSequence(topCusts)
        self.updateBestSequence(lowestSeqObj)
        self.numRoutes = len(self.bestSequence) + len(lowestSeqObj.projectedRoute)
        self.goldenRoutes = self.combineRoutes(self.bestSequence, \
                                               lowestSeqObj.projectedRoute)
        
    def updateBestSequence(self, seqObj):
        self.workingCustomers.remove(seqObj.customer)
        self.bestSequence.addNext(seqObj.vehicle, seqObj.customer)
    
    def lowestProjectedSequence(self, topCusts): 
        baseCost =  Cost.ofRoutes(self.bestSequence) 
        for top in topCusts:
            top.projectedRoute = self.heuristic.run(self.d, top.customer, \
                                                    self.workingCustomers, self.depot) 
            top.tCost = baseCost + \
                        Cost.vehicleToCustomer(top.vehicle, top.customer) + \
                        Cost.ofRoutes(top.projectedRoute)

        return min(topCusts, key = lambda x: x.tCost) 

    def combineRoutes(self, frontSequence, endSequence):
        # shallow copy might not copy the routes objects?!
        routes = deepcopy(frontSequence)
        if(endSequence[0][0].custNo != 0):
            restOfVehicle = endSequence.pop(0) 
            for cust in restOfVehicle[1:]:
                routes.last().append(cust)
        for route in endSequence:
            routes.objList.append(route)
       
        return routes

