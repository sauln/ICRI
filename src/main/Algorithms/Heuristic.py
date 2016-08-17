""" Base for H_g  """
import pickle
import sortedcontainers

from src.visualization.visualize import Plotter
from src.main.BaseObjects.Dispatch import Dispatch
from src.main.BaseObjects.Parameters import Parameters

class Heuristic:
    def __init__(self, dispatch):
        self.dispatch = dispatch

    def run(self):
        

        while self.dispatch.customers:
            vehicles = self.dispatch.getNextVehicles()
            nextFeas = self.dispatch.getFeasibles(vehicles) 
            vehicle, customer, cost = nextFeas[0]

            #print("For {:<8g} add {:<20} to {}".format(cost, customer.__str__(), vehicle))
            #print("{} customers left".format(len(self.dispatch.customers)))
            self.dispatch.addCustomer(vehicle, customer)

        return self.dispatch

if __name__ == "__main__":
    input_filepath = "data/interim/r101.p"
    with open(input_filepath, "rb") as f:
        sp = pickle.load(f)
   
    Parameters().build(sp, 10, 10)

    customers = sp.customers[1:]
    depot = sp.customers[0]

    dispatch = Dispatch(customers, depot)
    solution = Heuristic(dispatch).run()
    print(solution.solutionStr())
    
