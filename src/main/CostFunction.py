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
        return "pot next: {} {} {}".format(self.vehicle, self.customer, self.gnnhCost)
    def __repr__(self):
        return self.__str__()
    

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

    # these costs need to be better developed
    def c(self, routes, end=None):
        return 1

    def getBestNode(self, delta, customers, start):
        return self.lowestCostNext(start, delta, customers, 1)[0]
        #return self.getBestNNodes(cf, delta, customers, 1)[0]

    def getCostOfNext(self, delta, vehicle, customer):
        veh = vehicle if vehicle.isFeasible(customer) else Vehicle(Parameters().depot)
        cost = self.gnnh(delta, veh, customer) 
        return PotentialNextCustomer(veh, customer, cost)

    def lowestCostNext(self, vehicle, delta, customers, size):
        # replaces getBestNNodes when we have only 1 vehicle to consider 
        # this should go in vehicle



        #newVeh = Vehicle(Parameters().depot)
        cstest = sortedcontainers.SortedListWithKey(key=lambda x: x.gnnhCost)
        
        for cust in customers:
            cstest.add(self.getCostOfNext(delta, vehicle, cust))
        #for cust in customers:
        #    if(vehicle.isFeasible(cust)):
        #        cost = self.gnnh(delta, vehicle, cust) 
        #        cstest.add(PotentialNextCustomer(vehicle, cust, cost))
        #    else:
        #        cost = self.gnnh(delta, newVeh, cust) 
        #        cstest.add(PotentialNextCustomer(newVeh, cust, cost))
        
        
        return cstest[:size]

