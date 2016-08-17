import pickle
import time
import sys
import random
import logging
import sortedcontainers
from copy import copy, deepcopy

from src.main.Algorithms.Heuristic import Heuristic
from src.main.Algorithms.CostFunction import Cost
from src.main.BaseObjects.Dispatch import Dispatch
from src.main.BaseObjects.Parameters import Parameters
from src.main.BaseObjects.Vehicle import Vehicle

def genRandomDeltas(count):
    #random.seed(0)
    Delta = []
    for _ in range(count):
        Delta.append([random.random() for _ in range(7)])

    return Delta 

class RollOut:
    def __init__(self, dispatch):
        self.logger = logging.getLogger(__name__)
        #self.heuristic = Heuristic(dispatch)
        self.customers = Parameters().getCustomers()
        self.depot = Parameters().depot
        self.W = 100
        self.Delta = genRandomDeltas(2)
        self.workingRoutes = None
        self.numVehicles = self.minNumVeh = self.lowestCost = float("inf") 
        self.lowerLimit = 3

        self.dispatch = dispatch

    def duplicateEnv(self, dispatch, vehicle):
        # need to make a copy of the dispatch and copy of the vehicle
        # but also need the vehicle inside of dispatch
        # to be the same as this one
        tmpDispatch = Dispatch(dispatch)
        tmpVehicle = Vehicle(vehicle)
        tmpDispatch.vehicles = [v if v is not vehicle else tmpVehicle \
            for v in dispatch.vehicles]

        return tmpDispatch, tmpVehicle

    def run(self):
        print("Run rollout")

        for i in range(3):
            print(" * get next vehicles")
            vehicles = self.dispatch.getNextVehicles()

            print(" * get best next nodes")
            rankedCustomers = self.dispatch.getFeasibles(vehicles) 
            topCustomers = rankedCustomers[:2]
            
            lowestCost = float('inf')

            print(" * make a prediction using heuristic")
            for vehicle, customer, cost in topCustomers:    
                tmpDispatch, tmpVehicle = self.duplicateEnv(self.dispatch, vehicle)

                tmpDispatch.addCustomer(tmpVehicle, customer)
                potentialSolution = Heuristic(tmpDispatch).run()
                
                print("Projected solution: {}".format(potentialSolution.solutionStr()))

                if(Cost.ofSolution(potentialSolution) < lowestCost):
                    lowestCost = Cost.ofSolution(potentialSolution)
                    bestCustomer = customer
                    bestVehicle = vehicle

            print("Lowest cost: {}.  Add {} to {}."\
                .format(lowestCost, bestCustomer, bestVehicle))

            self.dispatch.addCustomer(bestVehicle, bestCustomer)

            print(self.dispatch.solutionStr())


        print(" * choose best")
        print(" * serve customer")

    
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

if __name__ == "__main__":
    input_filepath = "data/interim/r101.p"
    with open(input_filepath, "rb") as f:
        sp = pickle.load(f)

    Parameters().build(sp, 10, 10)

    customers = sp.customers[1:]
    depot = sp.customers[0]
    dispatch = Dispatch(customers, depot)

    RollOut(dispatch).run()


