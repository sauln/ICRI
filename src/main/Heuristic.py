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

    def run(self, delta, start, customers):
        self.setup(delta, start, customers)
        
        for i in range(len(self.customers)):
            top = self.costFunction.getBestNode(delta, self.routes.last(), self.customers)
            self.routes.addNext(top.vehicle, top.customer)
            self.customers.remove(top.customer)
       
        return self.routes 


