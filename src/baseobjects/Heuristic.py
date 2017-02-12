""" Base for H_g  """
import copy

from .Dispatch import Dispatch
from .Parameters import Parameters
from .Vehicle import Vehicle
from .CostFunction import Cost
from .Utils import *

class HeuristicWOnDeck:
    def run(self, dispatch, width=10, depth=10):
        dispatch = copy.deepcopy(dispatch)
        while dispatch.customers:
            vehicles = dispatch.get_available_vehicles(1)
            top_customers = dispatch.get_feasible_next_customers(vehicles, width)

            lowestCost, nexts = float("inf"), None
            for vehicle, customer, _ in top_customers:
                cost = Cost.gnnh(dispatch.delta, vehicle, customer)
                if cost < lowestCost:
                    nexts = (vehicle, customer)
                    lowestCost = cost

            veh, cust = nexts
            dispatch.add_customer(veh, cust)

        dispatch.finish()
        return dispatch

class Heuristic_greed:
    def run(self, dispatch, width=10, depth=10):
        while dispatch.customers:
            vehicles = dispatch.get_available_vehicles()
            top_customers = dispatch.get_feasible_next_customers(vehicles, width)

            lowestCost, nexts = float("inf"), None
            for vehicle, customer, _ in top_customers:
                cost = Cost.gnnh(dispatch.delta, vehicle, customer)
                if cost < lowestCost:
                    nexts = (vehicle, customer)
                    lowestCost = cost

            if nexts == None:
                newV = Vehicle(dispatch.depot)
                dispatch.vehicles.append(newV)
            else:
                veh, cust = nexts
                dispatch.add_customer(veh, cust)

        dispatch.finish()
        return dispatch


class Heuristic_sorted:
    '''  this heuristic forces adding to existing vehicle if feasible '''
    def run(self, dispatch, width=5, depth=5):
        cs = sorted(dispatch.customers, key=lambda x: x.readyTime)

        for customer in cs:
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
            veh.serve(cust)
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
            dispatch.add_customer(vehicle, customer)

        dispatch.finish()
        return dispatch
'''

class Heuristic(HeuristicWOnDeck):
    pass

if __name__ == "__main__":
    sp = open_sp("r101.p")
    Parameters().build(sp)
    dispatch = Dispatch(sp.customers)
    solution = Heuristic().run(dispatch)
    print(solution.pretty_print())



