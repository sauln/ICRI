""" Base for H_g  """
import sortedcontainers

from src.main.BaseObjects.Routes import Routes
from src.main.BaseObjects.Parameters import Parameters
from src.main.Algorithms.NextFinder import NextFinder 

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


