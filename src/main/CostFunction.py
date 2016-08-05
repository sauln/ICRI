import numpy as np
import sortedcontainers
from src.main.Parameters import Parameters
from src.main.Vehicle import Vehicle


class CostFunction():
    def __init__(self, heuristicType):
        self.switch = {"gnnh":self.gnnh, "distanceOnly":self.distanceOnly}
        self.heuristicType = heuristicType

    def run(self, *args):
        return self.switch[self.heuristicType](*args)

    def distanceOnly(self, delta, vehicle, end):
        return vehicle.travelDist(end)

    def gnnh(self, delta, vehicle, end): #s:start, e:end customers
        # Infeasible nodes would be filtered before here -
        nextArrivalTime = vehicle.totalTime + vehicle.travelTime(end)
        earliestService = max(nextArrivalTime, end.readyTime)

        c = np.zeros(len(delta))
        isDepot     = (vehicle.last().custNo == 0)
        travelDist  = vehicle.travelDist(end)
        remaining   = earliestService - vehicle.totalTime
        timeSlack   = end.dueDate - (vehicle.totalTime + vehicle.travelTime(end))
        capSlack    = (vehicle.maxCapacity - vehicle.curCapacity) - end.demand # slack

        c[0], c[1], c[2], c[3], c[4] = isDepot, travelDist, remaining, timeSlack, capSlack
        
        cost = np.dot(delta, c)    
        return cost 

    def getBestNode(self, delta, customers, start):
        return self.lowestCostNext(start, delta, customers, 1)[0]
        #return self.getBestNNodes(cf, delta, customers, 1)[0]

    def lowestCostNext(self, vehicle, delta, customers, size):
        # replaces getBestNNodes when we have only 1 vehicle to consider 
        # this should go in vehicle
        newVeh = Vehicle(Parameters().depot)
        cstest = sortedcontainers.SortedListWithKey(key=lambda x: x[2])
        for cust in customers:
            if(vehicle.isFeasible(cust)): 
                cstest.add((vehicle, cust, self.run(delta,vehicle,cust)))
            else:
                cstest.add((newVeh, cust, self.run(delta, newVeh, cust)))
        return cstest[:size]

