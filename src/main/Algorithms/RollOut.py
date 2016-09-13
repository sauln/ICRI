import pickle
import time
import sys
import random
import logging
import sortedcontainers
from copy import copy, deepcopy


from src.visualization.visualize import Plotter
from src.main.Algorithms.Heuristic import Heuristic_new
from src.main.Algorithms.CostFunction import Cost
from src.main.BaseObjects.Dispatch import Dispatch
from src.main.BaseObjects.Parameters import Parameters
from src.main.BaseObjects.Vehicle import Vehicle

import pdb
logger = logging.getLogger(__name__)

def genRandomDeltas(count):
    #random.seed(0)
    Delta = []
    for _ in range(count):
        Delta.append([random.random() for _ in range(7)])

    return Delta 

class RollOut:
    def __init__(self):
        #self.customers = Parameters().getCustomers()
        #self.depot = Parameters().depot
        self.W = 100
        #self.Delta = genRandomDeltas(2)
        self.workingRoutes = None
        self.numVehicles = self.minNumVeh = self.lowestCost = float("inf") 
        self.lowerLimit = 3

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
   
    
    '''
        want to implement in the loop heuristic tuning
          implementation like parallel heuristic - 

          choose new heuristics


    '''






    def rollHeuristicOut(self, dispatch, topCustomers):
        lowestCost = (float('inf'),float('inf'))
        for vehicle, customer, cost in topCustomers:    
            tmpDispatch, tmpVehicle = self.duplicateEnv(dispatch, vehicle)

            tmpDispatch.addCustomer(tmpVehicle, customer)
            potentialSolution = Heuristic_new().run(tmpDispatch)
            
            if(Cost.ofSolution(potentialSolution) < lowestCost):
                lowestCost = Cost.ofSolution(potentialSolution)
                bestCustomer = customer
                bestVehicle = vehicle
        return bestVehicle, bestCustomer, lowestCost




    def run(self, dispatch):
        dispatch = deepcopy(dispatch)

        logger.info("Run rollout")
        while dispatch.customers:
            vehicles = dispatch.getNextVehicles()
            rankedCustomers = dispatch.getFeasibles(vehicles) 
            topCustomers = rankedCustomers[:10]
            bestVehicle, bestCustomer, bestCost = \
                self.rollHeuristicOut(dispatch, topCustomers)
            dispatch.addCustomer(bestVehicle, bestCustomer)
           
        dispatch.finish()
        return dispatch
  

def run_roll_out():
    input_filepath = "data/interim/r101.p"
    with open(input_filepath, "rb") as f:
        sp = pickle.load(f)

    Parameters().build(sp, 10, 10)

    customers = sp.customers[1:]
    depot = sp.customers[0]
    dispatch = Dispatch(customers, depot)

    delta = [1]*7
    dispatch.set_delta(delta)
   
    print(dispatch.delta)
    solution = RollOut().run(dispatch)
    print(solution.solutionStr())
    
    output_filepath = "data/interim/SolutionR101.p"
    with open(output_filepath, "wb") as f:
        pickle.dump(solution, f)

    #Plotter().plotDispatch(solution).show()




if __name__ == "__main__":
    run_roll_out()
