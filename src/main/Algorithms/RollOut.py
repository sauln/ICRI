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

import pdb

def genRandomDeltas(count):
    #random.seed(0)
    Delta = []
    for _ in range(count):
        Delta.append([random.random() for _ in range(7)])

    return Delta 

class RollOut:
    def __init__(self, dispatch):
        self.logger = logging.getLogger(__name__)
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
        # to be the same as this one. copy, copy, replace
        
        tmpDispatch = Dispatch(dispatch)
        tmpVehicle = Vehicle(vehicle)
        tmpDispatch.vehicles = [v if v == tmpVehicle else tmpVehicle \
            for v in tmpDispatch.vehicles]
        if tmpVehicle not in tmpDispatch.vehicles:
            tmpDispatch.vehicles.append(tmpVehicle)

        return tmpDispatch, tmpVehicle
    
    def rollHeuristicOut(self, topCustomers):
        lowestCost = float('inf')
        for vehicle, customer, cost in topCustomers:    
            tmpDispatch, tmpVehicle = self.duplicateEnv(self.dispatch, vehicle)

            tmpDispatch.addCustomer(tmpVehicle, customer)
            potentialSolution = Heuristic(tmpDispatch).run()
            
            if(Cost.ofSolution(potentialSolution) < lowestCost):
                lowestCost = Cost.ofSolution(potentialSolution)
                bestCustomer = customer
                bestVehicle = vehicle
        return bestVehicle, bestCustomer, lowestCost

    def run(self):
        print("Run rollout")
        while self.dispatch.customers:
            vehicles = self.dispatch.getNextVehicles()
            rankedCustomers = self.dispatch.getFeasibles(vehicles) 
            topCustomers = rankedCustomers[:2]
            bestVehicle, bestCustomer, bestCost = self.rollHeuristicOut(topCustomers)
            self.dispatch.addCustomer(bestVehicle, bestCustomer)
            
        return self.dispatch
   

if __name__ == "__main__":
    input_filepath = "data/interim/r101.p"
    with open(input_filepath, "rb") as f:
        sp = pickle.load(f)

    Parameters().build(sp, 10, 10)

    customers = sp.customers[1:]
    depot = sp.customers[0]
    dispatch = Dispatch(customers, depot)

    solution = RollOut(dispatch).run()
    print(solution.solutionStr())


