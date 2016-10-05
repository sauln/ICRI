import numpy as np
from sortedcontainers import SortedListWithKey
from operator import itemgetter

from .Vehicle import Vehicle
from .Parameters import Parameters
from .Customer import Customer
from .CostFunction import Cost

class Dispatch():
    def __init__(self, customers, depot=None):
        ''' Dispatch will organize the vehicles '''
        ''' And organize the customers '''
        
        self.max_vehicles = 25
        if isinstance(customers, self.__class__):
            # copying from other dispatch
            dispatch = customers
            self.customers = list(dispatch.customers)
            self.depot = dispatch.depot
            self.visitedCustomers = list(dispatch.visitedCustomers)
            self.vehicles = [Vehicle(v) for v in dispatch.vehicles]
            self.delta = dispatch.delta
        else:
            if depot is None:
                depot = customers[0]
                customers = customers[1:]

            self.customers = list(customers)
            self.depot = depot
            self.visitedCustomers = [] 
            self.vehicles = []
            #self.vehicles = [self.new_vehicle() \
            #    for _ in range(self.max_vehicles)] 
            
            self.delta = None

    def get_available_vehicles(self):
        ''' Return set of vehicles that have not reached the depot 
             if no vehicles yet, return an empty vehicle
        '''
        vehicles = list(set(self.vehicles))
        if not vehicles:
            vehicles = [self.new_vehicle()]
        
        return vehicles 

        #vehicles = self.vehicles if self.vehicles else [self.new_vehicle()]
        # if they are all the empty
        #return vehicles 

    def get_feasible_next_customers(self, vehicles, count=None):
        next_pairs = [ (vehicle, customer, Cost.gnnh(self.delta, vehicle, customer)) \
                        for vehicle in vehicles \
                        for customer in self.customers \
                        if vehicle.isFeasible(customer) ]
        cs = SortedListWithKey(key=itemgetter(2))
        cs.update(next_pairs)
        return cs[:count]

    def add_customer(self, vehicle, customer):
        if vehicle not in self.vehicles:
            self.vehicles.append(vehicle)
        vehicle.serveCustomer(customer)

        self.customers.remove(customer)
    
    def set_delta(self, delta):
        self.delta = delta

    def finish(self):
        self.vehicles = [v for v in self.vehicles \
            if len(v.customerHistory) > 1]

        for vehicle in self.vehicles:
            vehicle.serveCustomer(self.depot)

    def new_vehicle(self):
         return Vehicle(self.depot)

    def solutionStr(self):
        vehstr = "\n".join([str(v) for v in self.vehicles])
        return "Vehicles: {} => \n{} ".format(len(self.vehicles), vehstr)

    def total_dist(self):
        return sum([v.totalDist for v in self.vehicles])


    ##############################################################
    #####     These should probably not be there
    #def dist(self, a,b):
    #    # all of the cost objects should be dynamics
    #    return np.sqrt((a.x-b.x)**2 + (a.y-b.y)**2)

    #def cost(self, start, c):
    #    # travel dist, measure of how much time remaining.
    #    return self.dist(start,c) + (c.end)

    ##############################################################

    #def isFeasible(self, a, b):
    #    import pdb; pdb.set_trace()
    #    return a.readyTime + self.dist(a.location, b.location) <= b.dueDate

    #def feasibleList(self, customer):
    #    return [c for c in self.customers  if self.isFeasible(customer, c) 
    #        and c is not customer]
