import numpy as np
from sortedcontainers import SortedListWithKey
from operator import itemgetter

from .Vehicle import Vehicle, vehicle_copy
from .Parameters import Parameters
from .Customer import Customer
from .CostFunction import Cost


def dispatch_copy(dispatch):
    ''' copying from other dispatch '''
    tmp = Dispatch(dispatch.customers)
    tmp.customers = list(dispatch.customers)
    tmp.depot = dispatch.depot
    tmp.visitedCustomers = list(dispatch.visitedCustomers)
    tmp.vehicles = [vehicle_copy(v) for v in dispatch.vehicles]
    tmp.delta = dispatch.delta
    tmp.capacity = dispatch.capacity
    return tmp


class Dispatch():
    def __init__(self, customers, depot=None):
        ''' Dispatch will organize the vehicles and customers'''
        self.max_vehicles = 25
        if depot is None:
            depot = customers[0]
            customers = customers[1:]

        self.customers = list(customers)
        self.depot = depot
        self.visitedCustomers = [] 
        self.vehicles = []
        self.capacity = Parameters().params.capacity
        self.delta = None

    def get_available_vehicles(self, clean_veh=0):
        ''' Return set of vehicles that have not reached the depot 
             if no vehicles yet, return an empty vehicle
        '''
        vehicles = list(set(self.vehicles))

        if clean_veh:
            if self.new_vehicle() not in vehicles:
                vehicles.append(self.new_vehicle())
        
        return vehicles 

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
        vehicle.serve(customer)

        self.customers.remove(customer)
    
    def set_delta(self, delta):
        self.delta = delta

    def finish(self):
        self.vehicles = [v for v in self.vehicles \
            if v.served_customers() > 1]

        for vehicle in self.vehicles:
            vehicle.serve(self.depot)

    def new_vehicle(self):
         return Vehicle(self.depot, self.capacity)

    def pretty_print(self):
        vehstr = "\n".join([str(v) for v in self.vehicles])
        return "Vehicles: {}=> \n{} ".format(Cost.of_vehicles(self.vehicles), vehstr)

    def total_dist(self):
        return sum([v.total_dist for v in self.vehicles])

