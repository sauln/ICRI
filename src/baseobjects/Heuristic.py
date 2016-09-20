""" Base for H_g  """
import pickle
import sortedcontainers

from .Dispatch import Dispatch
from .Parameters import Parameters
from .Vehicle import Vehicle
from .CostFunction import Cost

class Heuristic_new:
    def run(self, dispatch):
        cs = sorted(dispatch.customers, key=lambda x: x.readyTime)

        for customer in cs:
            # pdb.set_trace()
            lowestCost = float("inf")
            nexts = None
            for vehicle in dispatch.vehicles:
                if vehicle.isFeasible(customer): 
                    cost = Cost.gnnh(dispatch.delta, vehicle, customer) 
                    if cost < lowestCost:
                        nexts = (vehicle, customer)
                        lowestCost = cost

            if nexts == None:
                newV = Vehicle(dispatch.depot)
                dispatch.vehicles.append(newV)
                nexts = (newV, customer)

            veh, cust = nexts
            veh.serveCustomer(cust)
        dispatch.finish()
        return dispatch

'''
class Heuristic:
    def __init__(self):
        pass

    def run(self, dispatch):
        while dispatch.customers:
            vehicles = dispatch.getNextVehicles()
            nextFeas = dispatch.getFeasibles(vehicles) # ordered by g
            vehicle, customer, cost = nextFeas[0]
            dispatch.addCustomer(vehicle, customer)

        dispatch.finish()
        return dispatch
'''

if __name__ == "__main__":
    input_filepath = "data/interim/r101.p"
    with open(input_filepath, "rb") as f:
        sp = pickle.load(f)
   
    Parameters().build(sp, 10, 10)

    customers = sp.customers[1:]
    depot = sp.customers[0]

    dispatch = Dispatch(customers, depot)
    solution = Heuristic_new().run(dispatch)
    print(solution.solutionStr())
    # Plotter().plotDispatch(solution).show()
    # Plotter().vehicles3D(solution).show() 
    # Plotter().customers3D(customers).show() 
