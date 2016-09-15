import pickle
import time
import sys
import random
import logging
import sortedcontainers
from copy import copy, deepcopy


from src.visualization.visualize import Plotter
from src.main.Algorithms.Heuristic import Heuristic, Heuristic_new
from src.main.Algorithms.CostFunction import Cost
from src.main.BaseObjects.Dispatch import Dispatch
from src.main.BaseObjects.Parameters import Parameters
from src.main.BaseObjects.Vehicle import Vehicle

import pdb
logger = logging.getLogger(__name__)

class RollOut:
    def duplicateEnv(self, dispatch, vehicle):
        tmpDispatch = Dispatch(dispatch)
        tmpVehicle = Vehicle(vehicle)
        tmpDispatch.vehicles = [v if v != tmpVehicle else tmpVehicle \
            for v in tmpDispatch.vehicles]
        if tmpVehicle not in tmpDispatch.vehicles:
            tmpDispatch.vehicles.append(tmpVehicle)

        return tmpDispatch, tmpVehicle

    def rollHeuristicOut(self, dispatch, topCustomers):
        lowestCost = (float('inf'),float('inf'))
        for vehicle, customer, _ in topCustomers:    
            tmpDispatch, tmpVehicle = self.duplicateEnv(dispatch, vehicle)

            tmpDispatch.addCustomer(tmpVehicle, customer)
            potentialSolution = Heuristic_new().run(tmpDispatch)
            
            cost = Cost.ofSolution(potentialSolution)
            if(cost < lowestCost):
                lowestCost = cost
                bestCustomer = customer
                bestVehicle = vehicle
                bestSolution = potentialSolution
        return bestVehicle, bestCustomer, lowestCost, bestSolution

    def run(self, dispatch):
        dispatch = deepcopy(dispatch)

        logger.info("Run rollout")
        while dispatch.customers:
            vehicles = dispatch.getNextVehicles()
            rankedCustomers = dispatch.getFeasibles(vehicles) 
            topCustomers = rankedCustomers[:10]
            bestVehicle, bestCustomer, bestCost, bestSolution = \
                self.rollHeuristicOut(dispatch, topCustomers)
            dispatch.addCustomer(bestVehicle, bestCustomer)
           
        dispatch.finish()
        return dispatch
  
def load_sp(fname, root="data/interim/"):
    input_filepath = root + fname
    with open(input_filepath, "rb") as f:
        sp = pickle.load(f)

def save_sp(solution, fname, root="data/solution/"):
    output_filepath = root + fname 
    with open(output_filepath, "wb") as f:
        pickle.dump(solution, f)


def run_roll_out(ps):
    sp = load_sp(ps)

    Parameters().build(sp, 10, 10)

    customers = sp.customers[1:]
    depot = sp.customers[0]
    dispatch = Dispatch(customers, depot)

    delta = [1]*7
    dispatch.set_delta(delta)
   
    #print(dispatch.delta)
    solution = RollOut().run(dispatch)
    #print(solution.solutionStr())
    return solution
    #save_sp(solution, ps)

if __name__ == "__main__":
    run_roll_out("r101.p")
