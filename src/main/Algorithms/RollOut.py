import time
import sys
import random
import logging
import sortedcontainers
from copy import copy, deepcopy

from src.main.Algorithms.Heuristic import Heuristic
from src.main.Algorithms.CostFunction import Cost
from src.main.Algorithms.NextFinder import NextFinder

from src.main.BaseObjects.Routes import Routes
from src.main.BaseObjects.Parameters import Parameters

class RollOut:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.heuristic = Heuristic()
        self.pm = Parameters()
        self.depot = self.pm.depot

        # need to maintain two routes objects
        self.routes = Routes(self.depot)
        self.W = 100

        self.Delta = self.genRandomDeltas(20)
        self.workingRoutes = None
        
        self.numVehicles = self.minNumVeh = self.lowestCost = float("inf") 
        self.lowerLimit = 3

    def genRandomDeltas(self, count):
        random.seed(0)

        Delta = []
        for _ in range(count):
            Delta.append([random.random() for _ in range(7)])

        return Delta 
        
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
        #self.logger.info("Running roll out with delta: {}".format(delta)) 
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
                Cost.ofRoutes(top.projectedRoute)
                #Cost.vehicleToCustomer(top.vehicle, top.customer) + \

        return min(topCusts, key = lambda x: x.tCost) 

    def findMatch(self, frontSeq, backSeq):
        key = backSeq[0]
        for vehicle in frontSeq:
            if(vehicle.last() == key):
                return vehicle

    def combineRoutes(self, frontSequence, backSequence):
        # shallow copy might not copy the routes objects?!
        #self.logger.info("Combining routes {}\n and {} together".format(frontSequence, backSequence))
       
        routes = deepcopy(frontSequence)
        if(backSequence[0][0].custNo != 0):
            frontVehicle = self.findMatch(routes, backSequence[0])
            endVehicle = backSequence.pop(0) 
            for cust in endVehicle[1:]:
                frontVehicle.append(cust)
        for route in backSequence:
            routes.objList.append(route)
       
        return routes

