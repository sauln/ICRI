""" Base for H_g  """
import pickle
import sortedcontainers

from src.visualization.visualize import Plotter
from src.main.BaseObjects.Dispatch import Dispatch
from src.main.BaseObjects.Parameters import Parameters

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

if __name__ == "__main__":
    input_filepath = "data/interim/r101.p"
    with open(input_filepath, "rb") as f:
        sp = pickle.load(f)
   
    Parameters().build(sp, 10, 10)

    customers = sp.customers[1:]
    depot = sp.customers[0]

    dispatch = Dispatch(customers, depot)
    solution = Heuristic().run(dispatch)
    print(solution.solutionStr())
    Plotter().plotDispatch(solution).show()
    
