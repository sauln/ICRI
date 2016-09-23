import pickle
import time
import sys
import random
import logging
import sortedcontainers
from copy import copy, deepcopy

from .baseobjects import Dispatch, Cost, Parameters, Vehicle, Heuristic

import pdb
logger = logging.getLogger(__name__)

def load_sp(fname, root="data/interim/"):
    input_filepath = root + fname
    with open(input_filepath, "rb") as f:
        sp = pickle.load(f)
    return sp

def save_sp(solution, fname, root="data/solution/"):
    output_filepath = root + fname 
    with open(output_filepath, "wb") as f:
        pickle.dump(solution, f)

class Best:
    def __init__(self, cost, customer, vehicle, solution):
        self.cost = cost
        self.customer = customer
        self.vehicle = vehicle
        self.solution = solution
        
class RollOut:
    def duplicateEnv(self, dispatch, vehicle):
        tmpDispatch = Dispatch(dispatch)
        tmpVehicle = Vehicle(vehicle)
        tmpDispatch.vehicles = [v if v != tmpVehicle else tmpVehicle \
            for v in tmpDispatch.vehicles]
        if tmpVehicle not in tmpDispatch.vehicles:
            tmpDispatch.vehicles.append(tmpVehicle)

        return tmpDispatch, tmpVehicle

    def run(self, dispatch):
        dispatch = deepcopy(dispatch)

        logger.debug("Run rollout with deltas {}".format(dispatch.delta))
        while dispatch.customers:
            vehicles = dispatch.getNextVehicles()
            rankedCustomers = dispatch.getFeasibles(vehicles) 
            topCustomers = rankedCustomers[:10]
            
            best = Best( (float('inf'), float('inf')), None, None, None)
            for vehicle, customer, _ in topCustomers:    
                tmpDispatch, tmpVehicle = self.duplicateEnv(dispatch, vehicle)

                tmpDispatch.addCustomer(tmpVehicle, customer)
                potentialSolution = Heuristic.Heuristic_new().run(tmpDispatch)
                
                cost = Cost.ofSolution(potentialSolution)
                if(cost < best.cost):
                    best = Best(cost, customer, vehicle, potentialSolution)
            
            dispatch.addCustomer(best.vehicle, best.customer)
           
        dispatch.finish()
        return dispatch

def run_roll_out(ps):
    sp = load_sp(ps)
    Parameters().build(sp, 10, 10)

    dispatch = Dispatch(sp.customers)

    delta = [1]*7
    dispatch.set_delta(delta)
   
    print(dispatch.delta)
    solution = RollOut().run(dispatch)
    print(solution.solutionStr())
    return solution
    #save_sp(solution, ps)

if __name__ == "__main__":
    run_roll_out("r101.p")

