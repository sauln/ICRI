import time
import sys
import sortedcontainers
from copy import copy, deepcopy

from src.main.Vehicle import Vehicle
from src.main.Heuristic import Heuristic
from src.main.Routes import Routes
from src.main.Parameters import Parameters
from src.main.CostFunction import CostFunction


class RollOut:
    def __init__(self):
        self.heuristic = Heuristic()
        self.costFunction = CostFunction("gnnh")
        pm = Parameters()
        self.depot = pm.depot
        self.customers = list(pm.customers)

        # need to maintain two routes objects
        self.routes = Routes(self.depot)
        self.bestSequence = Routes(self.depot)

        # don't need 'start' because we can grab off end of list
        start = self.depot
        numVehicles = minNumVeh = lowestCost = float("inf") 
        lowerLimit = 12
        self.W = 100

        self.delta = [[10,1,1,1,1,1,1]]
        self.d = self.delta[0]
        
        self.goldenRoutes = None

    def constructRoute(self):
        lowestVehicle = self.bestSequence[-1]
        self.workingCustomers = list(self.customers)
        routes = self.rollOut()
        return routes 
   
    def rollOut(self):
        while len(self.workingCustomers) > 0: 
            self.rollOutNextCustomer() 
        self.goldenRoutes.finish()
        return self.goldenRoutes 

    def rollOutNextCustomer(self): 
        topCusts = self.costFunction.getBestNNodes(self.d, self.bestSequence[-1],  \
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
        baseCost =  self.costFunction.cRoutes(self.bestSequence) 
        for top in topCusts:
            top.projectedRoute = self.heuristic.run(self.d, top.customer, \
                                                    self.workingCustomers) 
            top.tCost = baseCost + \
                        self.costFunction.cCust(top.vehicle, top.customer) + \
                        self.costFunction.cRoutes(top.projectedRoute)

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

