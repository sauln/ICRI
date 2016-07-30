""" Base for H_g  """
from src.main.Routes import Routes
import sortedcontainers

from src.main.CostFunction import CostFunction

class Heuristic():
    def __init__(self, sp):
        self.sp = sp
        self.costFunction = CostFunction("gnnh")

    def setup(self, delta, start, customers, depot):
        self.delta      = delta
        self.customers  = list(customers) # shallow copy
        self.custBackup = list(customers)
        self.depot      = depot
        self.routes     = Routes(self.sp, start, self.depot)
        
        if start in customers: self.customers.remove(start)
        return self

    def buildSolution(self, delta, start, customers, depot):
        self.setup(delta, start, customers, depot)
        return self.run()
    
    def reset(self, start):
        self.setup(self.delta, start, self.custBackup, self.depot) 

    def run(self, depth = None):
        depth = min(len(self.customers), depth)
        
        for i in range(depth):
            vehicle, bestNext, cost = \
                self.routes.getBestNode(self.costFunction, self.delta, self.customers)
            self.routes.addNext(vehicle, bestNext)
            self.customers.remove(bestNext)
       
        self.routes.finish()
        return self.routes 

    def cost(self, delta, vehicle, c):
        return self.costFunction.run(delta, vehicle, c)

