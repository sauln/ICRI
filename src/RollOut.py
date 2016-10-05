import pickle
import logging
import copy
from abc import ABCMeta, abstractmethod

from .baseobjects import Dispatch, Cost, Parameters, Vehicle, Heuristic, Utils

logger = logging.getLogger(__name__)

class Best:
    def __init__(self, cost, customer, vehicle, solution):
        self.cost = cost
        self.customer = customer
        self.vehicle = vehicle
        self.solution = solution
class RollOutBase:
    __metaclass__ = ABCMeta

    @abstractmethod
    def rollout(self, count): pass
   
    def duplicateEnv(self, dispatch, vehicle):
        ''' Copy environment so we can modify dispatch at will for experimentation '''
        tmp_dispatch = Dispatch(dispatch)
        tmp_vehicle = Vehicle(vehicle)

        # this line has been the biggest pain in the rear.
        if tmp_vehicle in tmp_dispatch.vehicles:
            find = tmp_dispatch.vehicles.index(tmp_vehicle)
            tmp_dispatch.vehicles[find] = tmp_vehicle
        
        if tmp_vehicle not in tmp_dispatch.vehicles:
            tmp_dispatch.vehicles.append(tmp_vehicle)

        return tmp_dispatch, tmp_vehicle

    def setup_dispatch_env(self, dispatch, vehicle, customer):
        tmp_dispatch, tmp_vehicle = self.duplicateEnv(dispatch, vehicle)
        tmp_dispatch.add_customer(tmp_vehicle, customer)
        return tmp_dispatch

    def run(self, dispatch, depth=None, width=None):

        dispatch = copy.deepcopy(dispatch)
        logger.debug("Run rollout with deltas {}".format(dispatch.delta))
        
        dispatch = self.rollout(dispatch, depth, width) 
        dispatch.finish()
        
        logger.debug("Solution to rollout: {}, {}".format(\
            len(dispatch.vehicles), dispatch.total_dist())) 
        
        return dispatch 

class RollOutTypical(RollOutBase):
    def rollout(self, dispatch, depth, width):
        ''' Run rollout algorithm '''
        while dispatch.customers:
            vehicles = dispatch.get_available_vehicles()
            top_customers = dispatch.get_feasible_next_customers(vehicles, width) 

            best = Best( (float('inf'), float('inf')), None, None, None)
            for vehicle, customer, _ in top_customers:
                tmp_dispatch = self.setup_dispatch_env(dispatch, vehicle, customer)
                potentialSolution = Heuristic().run(tmp_dispatch, width=width, depth=depth)
                cost = Cost.of_vehicles(potentialSolution.vehicles)
                logger.debug("Heuristic result {} from {},{}".format(\
                    cost, customer, vehicle))
                if(cost < best.cost):
                    best = Best(cost, customer, vehicle, potentialSolution)

            if(best.vehicle is None or best.customer is None):
                v = Vehicle(dispatch.depot)
                dispatch.vehicles.append(v)
            else: 
                dispatch.add_customer(best.vehicle, best.customer)
           
        return dispatch

class RollOutLikeHeuristic(RollOutBase):
    def rollout(self, dispatch):
        customer_list = sorted(dispatch.customers, key=lambda x: x.dueDate)

        for c in customer_list:
            best = Best( (float('inf'), float('inf')), None, None, None)
            for v in dispatch.vehicles:

                tmp_dispatch = self.setup_dispatch_env(dispatch, v, c)
                tmp_solution = Heuristic().run(tmp_dispatch)
                
                cost = Cost.of_vehicles(tmp_solution.vehicles)
                if(cost < best.cost):
                    best = Best(cost, c, v, tmp_solution)
                    
            if best.vehicle == None:
                v = Vehicle(dispatch.depot)
                dispatch.vehicles.append(v)
                best = Best(None, c, v, None)
            
            dispatch.add_customer(best.vehicle, best.customer)

        return dispatch


class RollOut(RollOutTypical):
    pass
       

if __name__ == "__main__":
    run_rollout("r101.p")

