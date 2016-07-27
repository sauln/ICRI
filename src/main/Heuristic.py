
""" Base for H_g  """
from src.main.Routes import Routes
import sortedcontainers

from src.main.CostFunction import CostFunction


class Heuristic():
    def __init__(self, sp):
        self.sp = sp
        self.costFunction = CostFunction("gnnh", self.sp.timeMatrix, self.sp.distMatrix)

    def setup(self, delta, start, customers, depot):
        self.delta     = delta
        self.customers = list(customers) # shallow copy
        self.depot     = depot
        self.routes    = Routes(self.sp, start, self.depot)
        
        if start in customers: self.customers.remove(start)

    def buildSolution(self, delta, start, customers, depot):
        self.setup(delta, start, customers, depot)
        return self.run()

    def run(self):
        for i in range(len(self.customers)):
        #for i in range(3):
            vehicle, bestNext, cost = self.getBestNode()
            self.routes.addNext(vehicle, bestNext)
            self.customers.remove(bestNext)
        
        self.routes.finish()
        return self.routes 

    def cost(self, delta, vehicle, c):
        return self.costFunction.run(delta, vehicle, c)

    def getBestNode(self):
        return self.getBestNNodes(1)[0]

    def getBestNNodes(self, size):
        cs = sortedcontainers.SortedListWithKey(key=lambda x: x[2])
        
        # with lots of routes, this could become unreasonable
        # is there any faster way than to look at all of them?
        for vehicle in self.routes:
            for c in self.customers:
                if(vehicle.isFeasible(c)):
                    res = (vehicle, c, self.costFunction.run(self.delta, vehicle, c))  
                    cs.add(res)

        return cs[:size]

