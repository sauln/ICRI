""" Base for H_g  """
from src.main.Routes import Routes
import sortedcontainers

from src.main.Parameters import Parameters
from src.main.CostFunction import CostFunction

class Heuristic():
    def __init__(self):
        self.costFunction = CostFunction("gnnh")

    def setup(self, delta, start, customers):
        self.delta      = delta
        self.customers  = list(customers) # shallow copy
        self.custBackup = list(customers)
        self.depot      = Parameters().depot
        self.routes     = Routes(start, self.depot)
        
        if start in customers: self.customers.remove(start)
        #return self

    def run(self, delta, start, customers):
        # this should be in routes

        self.setup(delta, start, customers)
        
        for i in range(len(customers)):
            top = self.costFunction.getBestNode(delta, self.customers, self.routes.last())
            #self.routes.getBestNode(self.costFunction, delta, self.customers)
            print(top)

            self.routes.addNext(top.vehicle, top.customer)
            self.customers.remove(top.customer)
       
        self.routes.finish()
        return self.routes 


