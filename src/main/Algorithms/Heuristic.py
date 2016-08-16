""" Base for H_g  """
import pickle
import sortedcontainers

from src.visualization.visualize import Plotter
from src.main.BaseObjects.Dispatch import Dispatch
from src.main.BaseObjects.Parameters import Parameters

class Heuristic:
    def __init__(self, dispatch):
        self.dispatch = dispatch

    def run(self, delta, start, customers, depot):


        for i in range(100):
            vehicles = self.dispatch.getNextVehicles()
            nextFeas = self.dispatch.getFeasibles(vehicles) 
            vehicle, customer, cost = min(nextFeas, key = lambda x: x[2]) 
           
            # print("For {:<8g} add {:<20} to {}".format(cost, customer.__str__(), vehicle))
            # print("{} customers left".format(len(dispatch.customers)))
            dispatch.addCustomer(vehicle, customer)

        print(self.dispatch.solutionStr())

if __name__ == "__main__":
    input_filepath = "data/interim/r101.p"
    with open(input_filepath, "rb") as f:
        sp = pickle.load(f)
   
    Parameters().build(sp, 10, 10)

    customers = sp.customers[1:]
    depot = sp.customers[0]

    dispatch = Dispatch(customers, depot)
    
    Heuristic(dispatch).run([1]*7, depot, customers, depot)

