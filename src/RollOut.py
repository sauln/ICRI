import pickle
import logging
import copy

from .baseobjects import Dispatch, Cost, Parameters, Vehicle, Heuristic, Utils

logger = logging.getLogger(__name__)

class Best:
    def __init__(self, cost, customer, vehicle, solution):
        self.cost = cost
        self.customer = customer
        self.vehicle = vehicle
        self.solution = solution
        
class RollOut:
    def duplicateEnv(self, dispatch, vehicle):
        ''' Copy environment so we can modify dispatch at will for experimentation '''
        tmp_dispatch = Dispatch(dispatch)
        tmp_vehicle = Vehicle(vehicle)

        # this line has been the biggest pain in the rear.
        find = tmp_dispatch.vehicles.index(tmp_vehicle)
        if find < 0:
            tmp_dispatch.vehicles[find] = tmp_vehicle
        
        if tmp_vehicle not in tmp_dispatch.vehicles:
            tmp_dispatch.vehicles.append(tmp_vehicle)

        return tmp_dispatch, tmp_vehicle

    def setup_dispatch_env(self, dispatch, vehicle, customer):
        tmp_dispatch, tmp_vehicle = self.duplicateEnv(dispatch, vehicle)
        tmp_dispatch.addCustomer(tmp_vehicle, customer)
        return tmp_dispatch

    ''' Have rollout be identical to the heuristic? just have 
         the cost function be an application of the heuristic?
    ''' 

    def rollout_like_heuristic(self, dispatch):
        dispatch = copy.deepcopy(dispatch)
        logger.debug("Run rollout with deltas {}".format(dispatch.delta))
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
            
            dispatch.addCustomer(best.vehicle, best.customer)

        dispatch.finish()
        
        logger.debug("Solution to rollout: {}, {}".format(\
            len(dispatch.vehicles), dispatch.total_dist())) 
        return dispatch

    def run(self, dispatch, depth, width):
        #return self.rollout_like_heuristic(dispatch)
        return self.rollout_typical(dispatch, depth, width)

    def rollout_typical(self, dispatch, depth, width):
        ''' Run rollout algorithm '''
        dispatch = copy.deepcopy(dispatch)

        logger.debug("Run rollout with ({}, {}) and deltas {}".format(\
            depth, width, dispatch.delta))
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
                dispatch.addCustomer(best.vehicle, best.customer)
           
        dispatch.finish()

        logger.debug("Solution to rollout: {}, {}".format(\
            len(dispatch.vehicles), dispatch.total_dist()))


        return dispatch


if __name__ == "__main__":
    run_rollout("r101.p")

