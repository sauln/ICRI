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
        tmpDispatch = Dispatch(dispatch)
        tmpVehicle = Vehicle(vehicle)
        tmpDispatch.vehicles = [v if v != tmpVehicle else tmpVehicle \
            for v in tmpDispatch.vehicles]
        if tmpVehicle not in tmpDispatch.vehicles:
            tmpDispatch.vehicles.append(tmpVehicle)

        return tmpDispatch, tmpVehicle

    def run(self, dispatch):
        dispatch = copy.deepcopy(dispatch)

        logger.debug("Run rollout with deltas {}".format(dispatch.delta))
        while dispatch.customers:
            vehicles = dispatch.getNextVehicles()
            rankedCustomers = dispatch.getFeasibles(vehicles) 
            topCustomers = rankedCustomers[:10]
            
            best = Best( (float('inf'), float('inf')), None, None, None)
            for vehicle, customer, _ in topCustomers:    
                tmpDispatch, tmpVehicle = self.duplicateEnv(dispatch, vehicle)

                tmpDispatch.addCustomer(tmpVehicle, customer)
                potentialSolution = Heuristic().run(tmpDispatch)
                
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

