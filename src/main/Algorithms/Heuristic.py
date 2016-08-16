""" Base for H_g  """
import pickle
import sortedcontainers

from src.main.Algorithms.NextFinder import NextFinder 
from src.visualization.visualize import Plotter
from src.main.BaseObjects.Routes import Dispatch
from src.main.BaseObjects.Parameters import Parameters

class Heuristic():
    def __init__(self):
        pass
    
    def setup(self, delta, start, customers, depot):
        self.delta      = delta
        self.customers  = list(customers) # shallow copy
        self.depot      = depot
        self.routes     = Routes(start, self.depot)
        
        if start in customers: 
            self.customers.remove(start)

    def run(self, delta, start, customers, depot):
        for i in range(100):
            # print("get next vehicles")
            vehicles = dispatch.getNextVehicles()
            nextFeas = dispatch.getFeasibles(vehicles) 
            vehicle, customer, cost = min(nextFeas, key = lambda x: x[2]) 
           
            # print("For {:<8g} add {:<20} to {}".format(cost, customer.__str__(), vehicle))
            # print("{} customers left".format(len(dispatch.customers)))
            dispatch.addCustomer(vehicle, customer)

        print(dispatch.solutionStr())

if __name__ == "__main__":
    input_filepath = "data/interim/r101.p"
    with open(input_filepath, "rb") as f:
        sp = pickle.load(f)
   
    Parameters().build(sp, 10, 10)

    customers = sp.customers[1:]
    depot = sp.customers[0]
    dispatch = Dispatch(customers, depot)
    
    Heuristic().run([1]*7, depot, customers, depot)

