""" Base for H_g  """
from .Dispatch import Dispatch
from .Parameters import Parameters
from .Vehicle import Vehicle
from .CostFunction import Cost


class Heuristic:
    def run(self, dispatch):
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
    import Utils
    sp = Utils.load_sp(input_filepath, "")
    Parameters().build(sp)
    dispatch = Dispatch(sp.customers)
    solution = Heuristic().run(dispatch)
    print(solution.solutionStr())
