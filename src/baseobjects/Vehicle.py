import numpy as np
from .CostFunction import Cost

class TimeWindows(object):
    def __init__(self, depot, capacity):
        super(TimeWindows, self).__init__(depot, capacity)
        self.total_time = 0

    def isValidTime(self, customer):
        return self.total_time + self.travel_time(customer) <= customer.dueDate

    def travel_dist(self, customer):
        return Cost.euclidean_cust(self.last().location, customer.location)

    def travel_time(self, customer):
        return self.travel_dist(customer) 
    
    def canMakeItHomeInTime(self, customer):
        return self.total_time + self.travel_time(customer) + \
               Cost.euclidean_cust(customer.location, self.depot.location) <= \
               self.depot.dueDate
        
    def update_time(self, customer):
        arrivalTime = self.total_time + self.travel_time(customer)
        servedTime = max(arrivalTime, customer.readyTime)
        self.total_time = servedTime + customer.serviceLen


class Capacity(object):
    def __init__(self, depot, capacity):
        super(Capacity, self).__init__(depot, capacity)
        self.max_capacity = capacity
        self.cur_capacity = 0

    def update_capacity(self, customer):
        self.cur_capacity += customer.demand

    def is_not_full(self, customer):
        return self.max_capacity >= customer.demand + self.cur_capacity
    
    def remaining_slack(self):
        return self.max_capacity - self.cur_capacity

class CustomerHistory(object):
    def __init__(self, depot, capacity):
        super(CustomerHistory, self).__init__()
        self.customer_history = []
        self.depot = depot

    def update_history(self, customer):
        self.customer_history.append(customer)
    
    def served_customers(self):
        return len([c for c in self.customer_history if c.custNo is not 0])

    def last(self):
        return self.customer_history[-1]

    def geographicCenter(self):
        custs = set(self.customer_history)
        custs.remove(self.depot)
        coords = [[c.location.x, c.location.y] for c in custs]
        center = np.mean(coords, axis=0)
        return center

def vehicle_copy(vehicle):
    tmp = Vehicle(vehicle.depot, vehicle.max_capacity)
    tmp.total_dist = vehicle.total_dist
    tmp.total_time = vehicle.total_time
    tmp.cur_capacity = vehicle.cur_capacity
    tmp.customer_history = list(vehicle.customer_history)
    return tmp


class Vehicle(TimeWindows, Capacity, CustomerHistory):
    def __init__(self, depot, capacity):
        super(Vehicle, self).__init__(depot, capacity)            
        self.update_history(depot)
        self.total_dist = 0
    
    def isFeasible(self, customer):
        return self.isValidTime(customer) \
               and self.is_not_full(customer) \
               and self.canMakeItHomeInTime(customer)
    
    def serve(self, customer):
        self.total_dist += self.travel_dist(customer)
        self.update_time(customer)
        self.update_capacity(customer)
        self.update_history(customer)

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

    def feasibilityStr(self, item):
        return "isFeasible:{} ".format(self.isFeasible(item)) +\
               "is_not_full:{} ".format(self.is_not_full(item)) +\
               "isValidTime:{} ".format(self.isValidTime(item)) +\
               "canMakeItHome:{} ".format(self.canMakeItHomeInTime(item))

    def debugStr(self, item):
        return "\n\t\tItem {} is being added to \n\t\t{}; \n\t\t{}\n\
                totaltime: {}  travel_time:{:3g}  duedate:{}\n\
                maxCap: {}     demand:{}      curCap: {}".format(\
                item, self, self.feasibilityStr(item), \
                self.total_time, self.travel_time(item), item.dueDate, \
                self.max_capacity, item.demand, self.cur_capacity)
            
