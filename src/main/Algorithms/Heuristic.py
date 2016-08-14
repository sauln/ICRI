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
        self.setup(delta, start, customers, depot)

        

        for i in range(len(self.customers)):
            top = NextFinder.getBestNode(delta, self.routes, self.customers)
            self.routes.addNext(top.vehicle, top.customer)
            self.customers.remove(top.customer)
       
        return self.routes 

if __name__ == "__main__":
    input_filepath = "data/interim/r101.p"
    with open(input_filepath, "rb") as f:
        sp = pickle.load(f)
    
    #parameters = Parameters()
    #parameters.build(sp, 10, 20)
    
    
     
    
    customers = sp.customers[1:]
    depot = sp.customers[0]
    dispatch = Dispatch(customers, depot)
    
    for i in range(10):
        startNodes = dispatch.getRootNodes()

    




    #depot = sp.customers[0]
    #customers = sp.customers[1:]
    #delta = [1]*7
    #projectedRoute = Heuristic().run(delta, depot, customers, depot) 

    #Plotter().plotRoutes(projectedRoute).show()

