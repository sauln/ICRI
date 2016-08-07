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

    def constructRoute(self):
        routes = self.H_c() 
        return routes

    def H_c(self):
        lowestVehicle = self.bestSequence[-1]
        self.workingCustomers = list(self.customers)

        while len(self.workingCustomers) > 0: 
            #and lowerLimit < numVehicles and numVehicles <= minNumVeh:
            routes = self.rollOutNextCustomer() 
            numVehicles = len(routes)
        bestSequence.finish()
            
        return bestSequence
    
    def updateBestSequence(self, seqObj):
        self.workingCustomers.remove(seqObj.customer)
        self.bestSequence.addNext(seqObj.lowestVehicle, seqObj.lowestNext)
    
    def rollOutNextCustomer(self): 
        # there are multiple ways we can structure this
        topCusts = self.costFunction.lowestCostNext(self.bestSequence[-1],  self.d, \
                                                    self.workingCustomers,  5)

        lowestSeqObj = self.lowestProjectedSequence(topCusts)
        self.updateBestSequence(lowestSeqObj)
        routes = combineRoutes(self.bestSequence, lowestSeqObj.projectedRoute)
        return routes

    def lowestProjectedSequence(self, topCusts): 
        baseCost =  self.costFunction.c(self.bestSequence) 

        for top in topCusts:
            top.projectedRoute = self.heuristic.run(self.d, top.customer, \
                                                    self.workingCustomers) 
            top.tCost = baseCost + \
                        self.custFunction.c(top.vehicle, top.cust) + \
                        self.custFunction.c(projectedRoute)


        return min(topCusts, key = lambda x: x.tCost) 


    def combineRoutes(self, frontSequence, endSequence):
        # shallow copy might not copy the routes objects?!
        routes = deepcopy(frontSequence)
        if(endSequence[0][0].custNo != 0):
            lastVehicle = routes[-1]
            restOfVehicle = endSequence.pop(0) 
            for cust in restOfVehicle[1:]:
                lastVehicle.append(cust)
        
            assert lastVehicle != frontSequence[-1], "Need to make deeper copy"
            # last or first is depot - should be separate vehicles
        for route in endSequence:
            routes.objList.append(route)
        
        return routes



    '''
    def rollOut(self, heuristic, delta, customers, bests):
        pm = Parameters()
        ranked = sortedcontainers.SortedListWithKey(key=lambda x: x[1])
        for vehicle, bestNext, cost in bests:
            _t_routes = heuristic.run(delta, bestNext, customers, pm.depot, pm.searchDepth)
            nextCost = vehicle.travelDist(bestNext)
            solution = (_t_routes, _t_routes.cost() + nextCost , vehicle, bestNext)
            ranked.add(solution)

        return ranked[0]
    '''
    
