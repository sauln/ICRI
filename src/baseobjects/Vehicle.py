import numpy as np

from .Customer import Customer
from .Parameters import Parameters
#import Customer
#import Parameters


class TimeWindows(object):
    def __init__(self):
        super(TimeWindows, self).__init__()
        self.total_time = 0

    def isValidTime(self, end):
        return self.total_time + self.travel_time(end) <= end.dueDate
    
    def canMakeItHomeInTime(self, end):
        return end.dueDate + Parameters().travel_time(end, self.depot) <= self.depot.dueDate
        
    def update_time(self, customer):
        arrivalTime = self.total_time + self.travel_time(customer)
        servedTime = max(arrivalTime, customer.readyTime)
        #self.total_slack += servedTime - arrivalTime
        self.total_time = servedTime + customer.serviceLen



class Capacity(object):
    def __init__(self):
        super(Capacity, self).__init__()
        self.max_capacity = Parameters().params.capacity
        self.cur_capacity = 0

    def update_capacity(self, customer):
        self.cur_capacity += customer.demand

    def is_not_full(self, end):
        return self.max_capacity >= end.demand + self.cur_capacity
    
    def remaining_slack(self):
        return self.max_capacity - self.cur_capacity

class CustomerHistory(object):
    def __init__(self):
        super(CustomerHistory, self).__init__()
        self.customer_history = []

    def update_history(self, customer):
        self.customer_history.append(customer)
    
    def served_customers(self):
        return len([c for c in self.customer_history if c.custNo is not 0])

    def last(self):
        return self.customer_history[-1]


class Vehicle(TimeWindows, Capacity, CustomerHistory):
    def __init__(self, depot):
        super(Vehicle, self).__init__()

        # constructing with seed != depot is deprecated
        if isinstance(depot, self.__class__):
            vehicle = depot
            self.total_dist = vehicle.total_dist
            self.total_time = vehicle.total_time
            self.cur_capacity = vehicle.cur_capacity
            self.customer_history = list(vehicle.customer_history)
        else:
            self.update_history(depot)
            self.total_dist = 0
            #self.total_time, self.cur_capacity = 0,0 
            #self.served_customers() = 0
            
            #self.customer_history = [depot]
            #self.last_cust = depot
        
        self.timeMatrix = Parameters().timeMatrix
        self.distMatrix = Parameters().distMatrix
        self.depot = Parameters().depot
    
    
    def isFeasible(self, end):
        return self.isValidTime(end) and \
               self.is_not_full(end) #and \
               #self.canMakeItHomeInTime(end)
    
    def feasibilityStr(self, item):
        return "isFeasible:{} ".format(self.isFeasible(item)) +\
               "is_not_full:{} ".format(self.is_not_full(item)) +\
               "isValidTime:{} ".format(self.isValidTime(item)) +\
               "canMakeItHome:{} ".format(self.canMakeItHomeInTime(item))

    def __hash__(self):
        return hash((str(self.customer_history), self.total_dist, self.cur_capacity))

    def __eq__(self, other):
        return other is not None and \
               self.customer_history == other.customer_history and \
               self.total_dist       == other.total_dist and \
               self.cur_capacity     == other.cur_capacity

    def __str__(self):
        return "Veh: {}{}".format(self.served_customers(), \
            "["+", ".join(str(c.custNo) for c in self.customer_history) +"]", \
            self.total_dist, \
            self.last().custNo)
    
    def __repr__(self):
        return self.__str__()

    def serve(self, customer):
        self.total_dist += self.travel_dist(customer)
        self.update_time(customer)
        self.update_capacity(customer)
        self.update_history(customer)

    def travel_dist(self, end):
        return Parameters().travel_dist(self.last(), end) 

    def travel_time(self, end):
        return Parameters().travel_time(self.last(), end) 

    def geographicCenter(self):
        custs = set(self.customer_history)
        custs.remove(Parameters().depot)
        coords = [[c.location.x, c.location.y] for c in custs]
        center = np.mean(coords, axis=0)
        return center

    def debugStr(self, item):
        return "\n\t\tItem {} is being added to \n\t\t{}; \n\t\t{}\n\
                totaltime: {}  travel_time:{:3g}  duedate:{}\n\
                maxCap: {}     demand:{}      curCap: {}"\
            .format(item, self, self.feasibilityStr(item), \
                    self.total_time, self.travel_time(item), item.dueDate, \
                    self.max_capacity, item.demand, self.cur_capacity)
            
