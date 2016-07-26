
""" Base for H_g  """
from src.main.Routes import Routes
import sortedcontainers

import numpy as np

class Heuristic():
    def __init__(self, sp):
        self.sp = sp
        self.timeMatrix = sp.timeMatrix
        self.distMatrix = sp.distMatrix


    def buildSolution(self, delta, start, customers, depot):
        self.delta     = delta
        self.customers = list(customers) # shallow copy
        self.depot     = depot
        self.routes    = Routes(self.sp, start, self.depot)
        if start in customers: self.customers.remove(start)

        return self.run()


    def run(self):

        #for i in range(len(customers)):
        for i in range(3):
            vehicle, bestNext, cost = self.getBestNode()
            self.routes.addNext(vehicle, bestNext)
            self.customers.remove(bestNext)
        
        self.routes.finish()


        return self.routes 

    def getBestNode(self):
        return self.getBestNNodes(1)[0]
    """ Ranking algorithms """

    def getBestNNodes(self, size):
        cs = sortedcontainers.SortedListWithKey(key=lambda x: x[2])
        
        # with lots of routes, this could become unreasonable
        # is there any faster way than to look at all of them?

        for vehicle in self.routes:
            for c in self.customers:
                if(vehicle.isFeasible(c)):
                    res = (vehicle, c, self.heuristic(vehicle, c))  
                    cs.add(res)
       
        #if(len(cs) == 0):
        #    print("In the case of zero: \n\tcustomers: {}\n\troutes: {}\n\tdepot: {}"\
        #        .format(customers, routes, depot))

        #print("In getBestNNodes: {}".format(len(cs)))

        return cs[:size]


    def heuristic(self, vehicle, end): #s:start, e:end customers
        s = vehicle.lastCustomer()
        e = end

        # Infeasible nodes would be filtered before here -

        prevDeparture = vehicle.departureTime()
        nextArrivalTime = prevDeparture + self.sp.timeMatrix[s.custNo, e.custNo]
        earliestService = max(nextArrivalTime, e.readyTime)

        c = np.zeros(len(self.delta))
        c[0] = (s.custNo == 0)
        c[1] = self.distMatrix[s.custNo, e.custNo]
        c[2] = earliestService - prevDeparture
        c[3] = e.dueDate - (prevDeparture + self.timeMatrix[s.custNo,e.custNo])
        c[4] = vehicle.curCapacity - e.demand
        #d[5] = max(0, c_from.service_window[0] - earliest_possible_service)
        #d[6] = max(0, c_from_service_time - c_from.service_window[1])

        cost = np.dot(self.delta, c)    
        return cost 






