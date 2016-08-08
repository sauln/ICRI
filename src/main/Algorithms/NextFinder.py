import sortedcontainers
from src.main.Algorithms.CostFunction import Cost
from src.main.BaseObjects.Vehicle import Vehicle
from src.main.BaseObjects.Parameters import Parameters

#TODO pick a better name for NextFinder, this


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

class NextFinder:
    @staticmethod
    def getBestNode(delta, routes, customers):
        return NextFinder.getBestNNodes(delta, routes, customers, 1)[0]

    @staticmethod
    def getBestNNodes(delta, routes, customers, size):
        cstest = sortedcontainers.SortedListWithKey(key=lambda x: x.gnnhCost)
        
        for vehicle in routes: 
            for cust in customers:
                cstest.add(NextFinder.getCostOfNext(delta, vehicle, cust))
        return cstest[:size]
    
    @staticmethod
    def getCostOfNext(delta, vehicle, customer):
        veh = vehicle if vehicle.isFeasible(customer) else Vehicle(Parameters().depot)
        cost = Cost.gnnh(delta, veh, customer) 
        return PotentialNextCustomer(veh, customer, cost)


