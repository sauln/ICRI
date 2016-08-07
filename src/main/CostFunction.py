import numpy as np
import sortedcontainers
from src.main.Parameters import Parameters
from src.main.Vehicle import Vehicle

class PotentialNextCustomer:
    def __init__(self, vehicle, customer, gnnhCost):
        self.vehicle = vehicle
        self.customer = customer
        self.gnnhCost = gnnhCost
    def __str__(self):
        return "\nVehicle:{}\nCustomer:{}\nCost:{}".format(self.vehicle, self.customer, self.gnnhCost)
    def __repr__(self):
        return self.__str__()
    def __eq__(self, other):
        return self.vehicle == other.vehicle and \
               self.customer == other.customer and \
               self.gnnhCost == other.gnnhCost


class CostFunction():
    def __init__(self, heuristicType):
        self.switch = {"gnnh":self.gnnh, "distanceOnly":self.distanceOnly}
        self.heuristicType = heuristicType

    def appendingCost(self, delta, vehicle, end):
        return self.gnnh(delta, vehicle, end)

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

    def cCust(self, vehicle, end):
        return vehicle.travelTime(end)

    def cRoutes(self, routes):
        return len(routes)*10 

    def getBestNode(self, delta, vehicle, customers):
        return self.getBestNNodes(delta, vehicle, customers, 1)[0]

    def getBestNNodes(self, delta, vehicle, customers, size):
        cstest = sortedcontainers.SortedListWithKey(key=lambda x: x.gnnhCost)
        for cust in customers:
            cstest.add(self.getCostOfNext(delta, vehicle, cust))
        return cstest[:size]
    
    def getCostOfNext(self, delta, vehicle, customer):
        veh = vehicle if vehicle.isFeasible(customer) else Vehicle(Parameters().depot)
        cost = self.gnnh(delta, veh, customer) 
        return PotentialNextCustomer(veh, customer, cost)


