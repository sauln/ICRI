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
        self.pm = Parameters()
        self.depot = self.pm.depot

        # need to maintain two routes objects
        self.routes = Routes(self.depot)
        self.W = 100

        self.Delta = self.genRandomDeltas()


        self.workingRoutes = None
        
        self.numVehicles = self.minNumVeh = self.lowestCost = float("inf") 
        self.lowerLimit = 3

    def genRandomDeltas(self):
        return [[10,1,1,1,1,1,1], [1,1,1,1,1,1,1]]
        


    def constructRoute(self):
        for delta in self.Delta:
            self.bestSequence = Routes(self.depot)
            self.workingCustomers = Parameters().getCustomers() 
            tmpRoutes = self.rollOut(delta)
            if(tmpRoutes):
                routes = tmpRoutes
            self.minNumVeh = min(len(routes), self.minNumVeh)
        return routes 

    def solutionIsBestSoFar(self):
        return self.numVehicles <= self.lowerLimit
    
    def deltaIsTerrible(self):
        return self.minNumVeh < self.numVehicles

    def rollOut(self, delta):
        startNum = len(self.workingCustomers)
        while len(self.workingCustomers) > 0:
            if self.solutionIsBestSoFar():
                self.workingRoutes.finish()
                return self.workingRoutes
            
            if self.deltaIsTerrible():
                return None

            startNum -= 1
            self.rollOutNextCustomer(delta)
            self.numVehicles = len(self.workingRoutes)
             
        self.workingRoutes.finish()
        return self.workingRoutes 

    def rollOutNextCustomer(self, delta):
        topCusts = NextFinder.getBestNNodes(delta, self.bestSequence,  \
            self.workingCustomers,  5)

        lowestSeqObj = self.lowestProjectedSequence(topCusts, delta)
        self.updateBestSequence(lowestSeqObj)
        
        self.numRoutes = len(self.bestSequence) + len(lowestSeqObj.projectedRoute)
        self.workingRoutes = self.combineRoutes(self.bestSequence, \
            lowestSeqObj.projectedRoute)

        
    def updateBestSequence(self, seqObj):
        self.workingCustomers.remove(seqObj.customer)
        self.bestSequence.addNext(seqObj.vehicle, seqObj.customer)
    
    def lowestProjectedSequence(self, topCusts, delta): 
        baseCost =  Cost.ofRoutes(self.bestSequence) 
        for top in topCusts:
            top.projectedRoute = self.heuristic.run(delta, top.customer, \
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

