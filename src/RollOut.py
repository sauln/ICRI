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
        tmp_dispatch.vehicles = [v if v != tmp_vehicle else tmp_vehicle \
            for v in tmp_dispatch.vehicles]
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
       
        import pdb
        pdb.set_trace()
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

    def run(self, dispatch):
        #return self.rollout_like_heuristic(dispatch)
        return self.rollout_typical(dispatch)

    def rollout_typical(self, dispatch):
        ''' Run rollout algorithm '''
        dispatch = copy.deepcopy(dispatch)

        logger.debug("Run rollout with deltas {}".format(dispatch.delta))
        while dispatch.customers:
            ### Rollout should not be using _onDeck vehicle to add new vehicle
                        
            vehicles = dispatch.get_available_vehicles()
            top_customers = dispatch.get_feasible_next_customers(vehicles, 10) 

            best = Best( (float('inf'), float('inf')), None, None, None)
            for vehicle, customer, _ in top_customers:    
                tmp_dispatch = self.setup_dispatch_env(dispatch, vehicle, customer)
                potentialSolution = Heuristic().run(tmp_dispatch)
                
                cost = Cost.of_vehicles(potentialSolution.vehicles)
                if(cost < best.cost):
                    best = Best(cost, customer, vehicle, potentialSolution)

            dispatch.addCustomer(best.vehicle, best.customer)
           
        dispatch.finish()

        logger.debug("Solution to rollout: {}, {}".format(\
            len(dispatch.vehicles), dispatch.total_dist()))


        return dispatch

def run_roll_out(ps):
    sp = Utils.load_sp(ps)
    Parameters().build(sp)

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

